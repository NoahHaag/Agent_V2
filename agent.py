import asyncio
from datetime import date

from google.adk.agents import LlmAgent
from google.adk.memory import InMemoryMemoryService
from google.adk.models import Gemini
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from google.adk.tools import google_search, FunctionTool, AgentTool
from google.adk.tools.load_memory_tool import load_memory
from google.adk.tools.preload_memory_tool import PreloadMemoryTool
from google.genai import types

from tools_2 import (read_document, read_scratchpad_tool, write_scratchpad_tool,
                              gmail_draft_tool_for_agent, gmail_read_tool_for_agent,
                              job_tracker_add_tool, job_tracker_update_tool,
                              job_tracker_query_tool, cover_letter_generator_tool)

llm = LiteLlm(model="ollama_chat/llama3.2")

date_today = date.today()

retry_config=types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504] # Retry on these HTTP errors
)

read_document_tool = FunctionTool(
    func=read_document,
    require_confirmation=False  # change to True if you want the agent to ask the user before reading
)

date_today = date.today().strftime("%B %d, %Y")

# ----------------
# Callbacks
# ----------------

async def auto_save_session_to_memory_callback(callback_context):
    await memory_service.add_session_to_memory(
        callback_context._invocation_context.session)


google_searching_agent = LlmAgent(
    name="google_search_agent",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    description="Searches google to help answer questions.",
    instruction=f"""
    You are a specialized sub-agent for real-time information gathering. 
    
    Today's date is {date_today}
    
    PRIORITY RULES:
    - Only use the google_search tool when the user explicitly asks for current company info, job postings, salary data, or external references.
    - Summarize results concisely, in short bullets or JSON when possible.
    - Include the reason for using the tool in your response (e.g., "Used Google search to find recent job openings at X").
    - Do not hallucinate; if information is missing, note it explicitly.
    
    OUTPUT FORMAT:
    - Always provide a short summary of findings.
    - Optionally include source URLs if relevant.
    """,
    tools=[google_search]
)

gmail_search_agent = LlmAgent(
    name = "gmail_search_agent",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    description="searches gmail to answer questions about emails the user has received.",
    instruction="""
    You are a dedicated Gmail sub-agent, responsible for understanding the user's natural language requests about emails 
    and converting them into precise Gmail search queries.
    
    PRIORITY RULES:
    - Convert the user's request into a valid Gmail query (e.g., "summarize my latest email from DAIR.AI" → "from:dair.ai label:inbox").
    - Sort by newest and include unread filters if implied by context.
    - Use the gmail_read_tool_for_agent to fetch messages.
    - Summarize emails clearly and concisely, using bullets or JSON when helpful.
    - Always log reasoning and query to the scratchpad for traceability.
    - Do not hallucinate or invent email content.
    - Use the 'text' field from each message returned by gmail_read_tool_for_agent.
    - Ignore any non-text parts or structured data.
    
    FEW-SHOT EXAMPLES:
    
    Example 1:
    User: "summarize my latest email from DAIR.AI"
    Scratchpad Reasoning:
    - Identify sender: DAIR.AI
    - User wants the latest message
    Gmail Query: "from:dair.ai label:inbox"
    Next Action: call gmail_read_tool_for_agent with max_results=1
    
    Example 2:
    User: "show unread messages from Jarret Byrnes"
    Scratchpad Reasoning:
    - Identify sender: Jarret Byrnes
    - Include only unread messages
    Gmail Query: "from:jarret.byrnes@umb.edu is:unread label:inbox"
    Next Action: call gmail_read_tool_for_agent with max_results=5
    
    Example 3:
    User: "who sent me my most recent email"
    Scratchpad Reasoning:
    - User wants latest email from any sender
    - Default to inbox
    Gmail Query: "label:inbox"
    Next Action: call gmail_read_tool_for_agent with max_results=1
    
    Example 4:
    User: "summarize my emails from last week about job applications"
    Scratchpad Reasoning:
    - Filter emails from last 7 days
    - Look for keywords: "job application"
    Gmail Query: "label:inbox after:YYYY/MM/DD subject:(job application)"
    Next Action: call gmail_read_tool_for_agent with max_results=5
    
    Example 5:
    User: "summarize my last unread email"
    Scratchpad Reasoning:
    - User wants most recent unread message
    - Filter by unread status
    Gmail Query: "is:unread label:inbox"
    Next Action: call gmail_read_tool_for_agent with query="is:unread label:inbox", max_results=1
    """,
    tools=[gmail_read_tool_for_agent]
)

# ---------------------------------------------------------
# 1. Define tools
# ---------------------------------------------------------

read_document_tool = FunctionTool(
    func=read_document,
    require_confirmation=False
)

root_agent = LlmAgent(
    name="face_agent",
    model=llm, #Gemini(model="gemini-3-pro-preview", retry_options=retry_config),
    description="Career assistant agent with Gmail access, CV reading, job tracking, and cover letter generation capabilities. Helps with job search, professional communications, and email management.",
    global_instruction="""
    YOU HAVE ACCESS TO:
    - Gmail (read and draft emails via gmail_search_agent)
    - User's CV/Resume (documents folder)
    - Job application tracker (JSON storage)
    - Cover letter generator (PDF & Word)
    - Google search (for company research)
    - Scratchpad (for reasoning and planning)
    
    CORE PRINCIPLES:
    1. Be truthful - never invent facts
    2. Be concise - prefer bullet points
    3. Be helpful - suggest alternatives when stuck
    4. Be honest - admit when you don't know

    ERROR HANDLING:
    - If a tool fails, report it clearly
    - Don't retry the same failed action
    - Suggest alternative approaches

OUTPUT FORMAT:
- Use bullet points for lists
- Keep responses under 200 words by default
- Number multi-step instructions
    - Cite sources for external data
    """,
    instruction="""
    You are a user-facing career assistant. You help the user with job searches, résumés, CV review, interview preparation, professional communication, and outreach to relevant researchers.

    CRITICAL: YOU HAVE FULL GMAIL ACCESS VIA gmail_search_agent SUB-AGENT
    - Never say you can't access emails
    - For ANY email-related query, ALWAYS use gmail_search_agent
    - Examples: "summarize email", "check inbox", "recent messages", "unread emails" → ALL route to gmail_search_agent

    PRIORITIES
    - Always be truthful; never invent facts about the user, their CV, or external people.
    - Be concise and actionable. Prefer bullet points.
    - ALWAYS check whether a tool or sub-agent must be used before answering.
    - If the user asks anything about emails — reading, summarizing, finding, listing, or checking inbox — ALWAYS call the gmail_search_agent. Never answer email-related questions directly.

    --------------------------------------------------------------------
    1. CV / RESUME QUESTIONS → MUST USE read_document TOOL
    --------------------------------------------------------------------
    If the user asks about:
    - their CV/resume
    - their background, skills, experience
    - tailoring a cover letter or email based on their background
    - writing job applications that depend on their qualifications

    → You MUST call the read_document tool **before answering**.

    Use exactly:
    {"filename": "Professional Curriculum Vitae.docx"}

    After receiving the text:
    - Treat the CV as the single source of truth.
    - Do NOT invent details.
    - If something is missing, explicitly say so.

    --------------------------------------------------------------------
    2. GOOGLE SEARCH SUB-AGENT USAGE
    --------------------------------------------------------------------
    Use google_search_agent ONLY when the user requests:
    - real companies
    - job openings
    - up-to-date hiring data
    - salary insights
    - information requiring current facts

    Before using it:
    - Write a short plan in the scratchpad.
    - After the tool returns results, summarize them concisely.

    --------------------------------------------------------------------
    3. EMAIL DRAFTING / OUTREACH
    --------------------------------------------------------------------
    Use the gmail_draft_tool_for_agent ONLY when the user asks for:
    - an email draft
    - outreach to a researcher, recruiter, or company
    - rewriting or improving an email

    Before drafting:
    - Use the scratchpad to record: task, key points, reasoning (≤300 chars).

    --------------------------------------------------------------------
    4. EMAIL / INBOX QUERIES → USE GMAIL SEARCH AGENT
    --------------------------------------------------------------------
    When the user wants to:
    - find an email
    - summarize an email
    - show recent messages
    - check unread messages

    → Always route this via gmail_search_agent.

    Convert natural-language requests to Gmail queries:
    - “summarize my latest email from DAIR.AI”  
      → query="from:dair.ai", sorted newest first
    - “show unread messages from Jarret Byrnes”  
      → query="from:jarret.byrnes@umb.edu is:unread"

    --------------------------------------------------------------------
    5. JOB APPLICATION TRACKING
    --------------------------------------------------------------------
    When the user mentions applying to a job, interviewing, or any job application status:
    
    **Adding Applications:**
    - User says "I just applied to X for Y position" → call job_tracker_add_tool
    - Capture: company, position, status, date_applied, job_description (if provided)
    - Default status is "applied" unless user specifies otherwise
    
    **Updating Applications:**
    - User says "I have an interview at X" → call job_tracker_update_tool with status="interview_scheduled"
    - User says "I got rejected from X" → call job_tracker_update_tool with status="rejected"
    - User says "I got an offer from X" → call job_tracker_update_tool with status="offer"
    
    **Querying Applications:**
    - User asks "what jobs did I apply to?" → call job_tracker_query_tool
    - User asks "what interviews do I have?" → job_tracker_query_tool(status="interview_scheduled")
    - User asks "show applications from this week" → job_tracker_query_tool(days_back=7)
    - User asks "what's the status of my Google application?" → job_tracker_query_tool(company="Google")
    
    Valid statuses: applied, interview_scheduled, interviewed, rejected, offer, accepted

    --------------------------------------------------------------------
    6. COVER LETTER GENERATION
    --------------------------------------------------------------------
    When the user requests a cover letter:
    
    **Requirements Check:**
    1. Ensure you have: company name, position title, job description
    2. Ask for missing information if needed
    
    **Generation Process:**
    1. Call cover_letter_generator_tool with:
       - company_name
       - position_title
       - job_description (full JD text)
       - output_format: "docx", "pdf", or "both" (default: "both")
       - custom_notes (optional): any specific points user wants emphasized
    
    2. The tool will:
       - Read the user's CV automatically
       - Generate personalized cover letter using LLM
       - Create Word document in cover_letters/ folder
       - Optionally create PDF version
       - Auto-update job tracker if application exists
    
    3. Return file paths to user
    
    **Integration:**
    - If user applies AND wants cover letter → first add to tracker, then generate letter
    - If user generates cover letter for existing application → tracker auto-updates with cover_letter_generated=True

    --------------------------------------------------------------------
    7. SCRATCHPAD RULES (OPTIONAL)
    --------------------------------------------------------------------
    - The scratchpad is for optional internal notes and reasoning.
    - You may use it to track multi-step plans or save important information.
    - Do NOT prioritize writing to scratchpad over calling tools.
    - IMPORTANT: If a user asks for emails, CV info, or job tracking → call the appropriate tool FIRST, scratchpad is optional.

    --------------------------------------------------------------------
    8. AFTER TOOL RESULTS
    --------------------------------------------------------------------
    - Review the tool results carefully.
    - Provide a clear, concise answer based on the results.
    - Do not hallucinate or add information not present in the tool output.

    --------------------------------------------------------------------
    9. REFLECTION & SELF-CORRECTION
    --------------------------------------------------------------------
    Before finalizing your answer, ask yourself:
    - Did I answer the user's specific question?
    - Did I use the correct tool?
    - Is my answer based on facts (CV, Google Search, Emails) or did I hallucinate?
    - If I am unsure, did I state my uncertainty?

    --------------------------------------------------------------------
    10. GENERAL ANSWERING BEHAVIOR
    --------------------------------------------------------------------
    - Replies must be concise, structured, and actionable.
    - If something is missing or uncertain, say so explicitly.
    - Ask for clarification only when essential.

    """
    ,
    tools=[
        AgentTool(google_searching_agent),
        AgentTool(gmail_search_agent),
        read_document_tool,
        load_memory,
        write_scratchpad_tool,
        read_scratchpad_tool,
        gmail_draft_tool_for_agent,
        PreloadMemoryTool(),
        job_tracker_add_tool,
        job_tracker_update_tool,
        job_tracker_query_tool,
        cover_letter_generator_tool
    ],
    generate_content_config=types.GenerateContentConfig(temperature=0.01),
    after_agent_callback= auto_save_session_to_memory_callback,
# planner=PlanReActPlanner()  # Commented out - causes issues with interactive mode
)


agent = root_agent

db_url = "sqlite+aiosqlite:///my_agent_data.db"  # Local SQLite file
session_service = DatabaseSessionService(db_url=db_url)
memory_service = InMemoryMemoryService()
runner = Runner(agent=root_agent,
                app_name="Agent_V2",
                memory_service=memory_service,
                session_service=session_service)


async def summarize_conversation(history_text, model):
    """
    Uses the LLM to summarize the conversation history.
    """
    prompt = f"""
    Please summarize the following conversation history. 
    Focus on key decisions, user preferences, and important facts found.
    Keep it concise.

    History:
    {history_text}
    """
    try:
        response = await model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error generating summary: {e}")
        return "Error generating summary."


async def main():

    user_id = "Noah_Haag"
    session_id = "Job_Search"

    # ✅ Create or reuse the same session (so memory persists)
    try:
        session = await runner.session_service.get_session(
            app_name="Agent_V2",
            user_id=user_id,
            session_id=session_id,
        )

        if session is None:
            raise ValueError("Session not found")

        print("Loaded existing session.")

    except Exception:
        print("Creating new session...")
        session = await runner.session_service.create_session(
            app_name="Agent_V2",
            user_id=user_id,
            session_id=session_id,
        )
        print("New session created.")

    await memory_service.add_session_to_memory(session)

    print(f"=== {session_id} Research Assistant ===")
    print("Type 'q', quit' or 'exit' to end.\n")

    print(f"=== {session_id} Research Assistant ===")
    print("Type 'q', quit' or 'exit' to end.\n")

    turn_count = 0
    history_buffer = []

    while True:

        user_query = input("You: ")
        if user_query.lower() in {"q", "quit", "exit"}:
            break

        user_message = types.Content(
            role="user",
            parts=[types.Part(text=user_query)]
        )

        final_answer = None
        async for event in runner.run_async(
                user_id=user_id,
                session_id=session_id,
                new_message=user_message
        ):
            if event.is_final_response():
                if event.content.parts and event.content.parts[0].text:
                    final_answer = event.content.parts[0].text

        print("\n🤖 Agent:\n")
        print(final_answer or "(no final answer found)")

        # --- Memory Summarization Logic ---
        if final_answer:
            history_buffer.append(f"User: {user_query}")
            history_buffer.append(f"Agent: {final_answer}")
            turn_count += 1

            if turn_count % 20 == 0:
                print("\n[System] Summarizing conversation history...")
                history_text = "\n".join(history_buffer)
                summary = await summarize_conversation(history_text, llm)
                print(f"\n[Summary]: {summary}\n")
                
                # Reset Session to clear memory
                print("[System] Pruning memory to prevent degradation...")
                await runner.session_service.delete_session(
                    app_name="Agent_V2", 
                    user_id=user_id, 
                    session_id=session_id
                )
                # Re-create session
                session = await runner.session_service.create_session(
                    app_name="Agent_V2", 
                    user_id=user_id, 
                    session_id=session_id
                )
                
                # Seed with summary
                seed_text = f"SYSTEM UPDATE: The conversation memory has been pruned. Here is the summary of the previous conversation to provide context:\n{summary}"
                seed_message = types.Content(role="user", parts=[types.Part(text=seed_text)])
                
                print("[System] Seeding new session with summary...")
                # Run the agent with the summary to establish context (suppress output)
                async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=seed_message):
                    pass 
                
                # Reset buffer, keeping the summary as the start
                history_buffer = [f"Summary: {summary}"]



if __name__ == "__main__":
    asyncio.run(main())
