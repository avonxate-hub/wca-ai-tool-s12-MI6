import os
import json
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

Every response MUST be valid JSON.

Use exactly this structure:

{
    "message": "string",
    "priority": "low, medium, or high",
    "recommendations": ["string"]
}

Rules:
- "message" must contain a useful, summarized , short response to the shop owner.
- "priority" must be exactly "low", "medium", or "high".
- "recommendations" must be a list of useful actions.
- Do not include Markdown.
- Do not include code fences.
- Do not include any text outside the JSON object.
"""

conversation_history = []

def validate_ai_response(ai_message):
    try:
        data = json.loads(ai_message)

        if not isinstance(data, dict):
            return None

        required_fields = [
            "message",
            "priority",
            "recommendations"
        ]

        for field in required_fields:
            if field not in data:
                return None

            if not data[field]:
                return None

        if data["priority"] not in ["low", "medium", "high"]:
            return None

        if not isinstance(data["recommendations"], list):
            return None

        return data

    except (json.JSONDecodeError, TypeError):
        return None
while True:

    print("\n================================")
    print("       DUKA STOCK ADVISOR")
    print("================================")
    print("1. Start New Session")
    print("2. Open Past Session")
    print("3. Exit")

    choice = input("\nChoose an option: ")

    if choice == "1":
        print("\nStarting a new session...")

        conversation_history = []

        while True:
            user_message = input("\nYou: ")

            if user_message.lower() == "exit":
                print("Leaving session...")
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

            ai_data = validate_ai_response(ai_message)

            if ai_data is None:
                print("Warning: AI returned invalid JSON. Retrying...")

                retry_response = client.models.generate_content(
                    model="gemini-3.5-flash-lite",
                    contents=conversation_history,
                    config=types.GenerateContentConfig(
                        system_instruction=system_prompt
                    )
                )

                ai_message = retry_response.text
                ai_data = validate_ai_response(ai_message)

                if ai_data is None:
                    print("Error: AI returned invalid JSON after retry.")
                    conversation_history.pop()
                    continue

            conversation_history.append(
                types.Content(
                    role="model",
                    parts=[types.Part.from_text(text=ai_message)]
                )
            )

            print(ai_message)

    elif choice == "2":
        print("\nPast sessions are not available yet.")

    elif choice == "3":
        print("\nGoodbye!")
        break

    else:
        print("\nInvalid option. Please choose 1, 2, or 3.")