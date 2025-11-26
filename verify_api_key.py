import os
import asyncio
from google.genai import Client
from dotenv import load_dotenv

load_dotenv()

async def main():
    # 1. Get API Key
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ Error: GOOGLE_API_KEY environment variable is not set.")
        print("   Please run: $env:GOOGLE_API_KEY='your_key_here'")
        return

    # 2. Strip whitespace/quotes (just like in agent.py)
    api_key = api_key.strip().strip('"').strip("'")
    
    print(f"🔑 Testing API Key: {api_key[:4]}...{api_key[-4:]}")
    print(f"📏 Length: {len(api_key)}")
    
    # 3. Try to generate content
    try:
        print("\n⏳ Connecting to Google GenAI...")
        client = Client(api_key=api_key)
        
        print("📤 Sending request to model 'gemini-2.5-flash-lite'...")
        response = await client.aio.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents="Hello! Are you working?"
        )
        
        print("\n✅ SUCCESS! The API key is valid.")
        print(f"🤖 Response: {response.text}")
        
    except Exception as e:
        print("\n❌ FAILURE! The API key was rejected.")
        print(f"⚠️ Error details: {e}")
        print("\nPossible causes:")
        print("1. The key is invalid or deleted.")
        print("2. The 'Generative Language API' is not enabled in Google Cloud Console.")
        print("3. The key has IP restrictions that block your current IP.")
        print("4. The model name 'gemini-2.5-flash-lite' is not available for your key/region.")

if __name__ == "__main__":
    asyncio.run(main())
