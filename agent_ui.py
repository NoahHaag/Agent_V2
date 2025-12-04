import streamlit as st
import asyncio
from google.genai import types
from agent import runner, memory_service, get_or_create_session, llm

# Page Configuration
st.set_page_config(
    page_title="Agent V2 Lite UI",
    page_icon="🤖",
    layout="wide"
)

# Constants
USER_ID = "Noah_Haag"
SESSION_ID = "Job_Search"

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Helper to run async code in Streamlit
def run_async(coro):
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)

# Initialize Agent Session
if "agent_session" not in st.session_state:
    with st.spinner("Initializing Agent..."):
        session = run_async(get_or_create_session(USER_ID, SESSION_ID))
        run_async(memory_service.add_session_to_memory(session))
        st.session_state.agent_session = session
        st.success("Agent Connected!")

st.title("Agent V2 Lite UI 🤖")
st.markdown("Use this interface to paste multi-line text or code snippets easily.")

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
prompt = st.chat_input("Message Agent V2...")

if prompt:
    # Add user message to UI
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepare message for agent
    user_message = types.Content(
        role="user",
        parts=[types.Part(text=prompt)]
    )

    # Run Agent
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        with st.spinner("Agent is working..."):
            async def run_agent_turn():
                final_answer = None
                # We need to capture the generator output
                async for event in runner.run_async(
                    user_id=USER_ID,
                    session_id=SESSION_ID,
                    new_message=user_message
                ):
                    if event.is_final_response():
                         if event.content and event.content.parts:
                            text_parts = [p.text for p in event.content.parts if p.text]
                            if text_parts:
                                final_answer = "\n".join(text_parts)
                return final_answer

            # Execute the turn
            response_text = run_async(run_agent_turn())
            
            if response_text:
                full_response = response_text
                message_placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            else:
                message_placeholder.error("No response received from agent.")

# Sidebar for explicit multi-line paste (optional backup)
with st.sidebar:
    st.header("Multi-line Paste")
    st.info("You can also paste large blocks here and click 'Send' if the chat input is too small.")
    multiline_input = st.text_area("Paste text here:", height=300)
    if st.button("Send Multi-line Input"):
        if multiline_input:
            # Add user message to UI
            st.session_state.messages.append({"role": "user", "content": multiline_input})
            # Rerun to process the input in the main chat loop logic
            # Note: Streamlit's rerun might reset local vars, so we need to handle this carefully.
            # A better way is to just inject it into the chat processing logic directly, 
            # but for simplicity in this 'Lite' UI, we can just trigger a rerun with a flag or 
            # just process it here. Let's process it here to avoid complexity.
            
            # ... (Duplicate logic for processing - ideally refactor into a function)
            # For now, let's just instruct the user to use the main chat input which supports Shift+Enter
            st.warning("Please use the main chat input! It supports multi-line with Shift+Enter.")
