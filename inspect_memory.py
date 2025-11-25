import asyncio
from google.adk.runners import Runner
from google.adk.memory import InMemoryMemoryService
from google.adk.sessions import DatabaseSessionService
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.genai import types

async def inspect_session_after_run():
    # Setup minimal runner
    llm = LiteLlm(model="ollama_chat/llama3.2")
    agent = LlmAgent(name="test", model=llm, description="test", instruction="test")
    memory_service = InMemoryMemoryService()
    session_service = DatabaseSessionService(db_url="sqlite+aiosqlite:///test_inspect.db")
    runner = Runner(agent=agent, app_name="test", memory_service=memory_service, session_service=session_service)

    # Create session
    try:
        session = await runner.session_service.create_session(app_name="test", user_id="user", session_id="test_session_v4")
    except Exception:
        session = await runner.session_service.get_session(app_name="test", user_id="user", session_id="test_session_v4")

    # Run one turn
    user_message = types.Content(role="user", parts=[types.Part(text="Hello")])
    async for event in runner.run_async(user_id="user", session_id="test_session_v4", new_message=user_message):
        pass

    # Inspect session again
    print("\nSession Events after run:", len(session.events))
    if session.events:
        print("First event:", session.events[0])

if __name__ == "__main__":
    asyncio.run(inspect_session_after_run())
