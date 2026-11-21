import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

system_prompt = """
You are the Duka Stock Advisor, an AI assistant designed to help
small shop owners manage their stock.

Your job is to:
- Understand information provided about shop inventory.
- Identify items that may need restocking.
- Give practical and clear advice.
- Prioritize important stock issues.
- Ask for clarification when the information is insufficient.

Keep your responses simple, practical, and useful to a Kenyan shop owner.
"""

conversation_history = []

while True:

    user_message = input("\nYou: ")

    if user_message.lower() == "exit":
        print("Goodbye!")
        break

    conversation_history.append(
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=user_message)]
        )
    )

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=conversation_history,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt
        )
    )

    ai_message = response.text

    conversation_history.append(
        types.Content(
            role="model",
            parts=[types.Part.from_text(text=ai_message)]
        )
    )

    print(f"\nDuka Advisor: {ai_message}")