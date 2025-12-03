import os
import asyncio
from dotenv import load_dotenv
from google import genai
from google.genai import types
import PyPDF2

# Load environment variables
load_dotenv()

# Configuration
MODEL_ID = "gemini-2.0-flash-001" # Using 2.0 Flash as 2.5 is not standard/public yet
RESUME_PATH = "public/Resume.pdf"

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    text = ""
    try:
        with open(pdf_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() + "\n"
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None
    return text

async def main():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GOOGLE_API_KEY not found in environment variables.")
        return

    # Initialize Gemini Client
    client = genai.Client(api_key=api_key)

    # Load Resume
    print(f"Loading resume from {RESUME_PATH}...")
    resume_text = extract_text_from_pdf(RESUME_PATH)
    
    if not resume_text:
        print("Failed to load resume content. Exiting.")
        return

    print("Resume loaded successfully.")

    # System instruction with resume context
    system_instruction = f"""You are a helpful assistant for Noah Haag.
You have access to Noah's resume context below.
Answer questions about Noah's experience, skills, and background based on this information.
Be concise and professional.

RESUME CONTEXT:
{resume_text}
"""

    # Start Chat Session
    try:
        chat = client.aio.chats.create(
            model=MODEL_ID,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.7,
            )
        )
        
        print(f"\n--- Gemini Lite Agent ({MODEL_ID}) ---")
        print("Type 'exit', 'quit', or 'q' to end the session.\n")

        while True:
            user_input = input("You: ").strip()
            if user_input.lower() in ["exit", "quit", "q"]:
                break
            
            if not user_input:
                continue

            response = await chat.send_message(user_input)
            print(f"Agent: {response.text}\n")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())
