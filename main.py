import os
import json
from datetime import datetime
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

summary_prompt = """
You are the session summarizer for the Duka Stock Advisor.

Review the conversation provided and produce a concise summary
of the shop owner's session.

Your summary must be valid JSON.

Use exactly this structure:

{
    "summary": "string",
    "key_stock_issues": ["string"],
    "recommended_actions": ["string"]
}

Rules:
- "summary" must briefly describe what happened during the session.
- "key_stock_issues" must contain the important stock issues discussed.
- "recommended_actions" must contain the most important actions suggested during the session.
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


def wants_raw_json(user_message):
    return "json" in user_message.lower()


def print_ai_response(ai_data):
    print("\nMESSAGE:")
    print(ai_data["message"])

    print("\nPRIORITY:")
    print(ai_data["priority"].upper())

    print("\nRECOMMENDATIONS:")
    for recommendation in ai_data["recommendations"]:
        print(f"• {recommendation}")


def print_session_summary(summary_data):
    if summary_data is None:
        print("Summary unavailable.")
        return

    print(f"\nSummary:")
    print(summary_data["summary"])

    print("\nKey Stock Issues:")
    if summary_data["key_stock_issues"]:
        for issue in summary_data["key_stock_issues"]:
            print(f"• {issue}")
    else:
        print("• None")

    print("\nRecommended Actions:")
    if summary_data["recommended_actions"]:
        for action in summary_data["recommended_actions"]:
            print(f"• {action}")
    else:
        print("• None")


def generate_session_summary(conversation_history):
    try:
        summary_history = conversation_history.copy()

        summary_history.append(
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(
                        text="Please summarize the entire shop-owner session according to the summary requirements."
                    )
                ]
            )
        )

        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=summary_history,
            config=types.GenerateContentConfig(
                system_instruction=summary_prompt
            )
        )

        summary_message = response.text

        summary_data = json.loads(summary_message)

        if not isinstance(summary_data, dict):
            return None

        required_fields = [
            "summary",
            "key_stock_issues",
            "recommended_actions"
        ]

        for field in required_fields:
            if field not in summary_data:
                return None

            if not summary_data[field]:
                return None

        if not isinstance(summary_data["key_stock_issues"], list):
            return None

        if not isinstance(summary_data["recommended_actions"], list):
            return None

        return summary_data

    except (json.JSONDecodeError, TypeError):
        return None
    except Exception:
        print("\nError: Unable to generate the session summary.")
        return None


def save_session(conversation_history, summary_data):
    os.makedirs("sessions", exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"sessions/session_{timestamp}.json"

    session_data = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "time": datetime.now().strftime("%H:%M:%S"),
        "conversation": [],
        "summary": summary_data
    }

    for message in conversation_history:
        session_data["conversation"].append({
            "role": message.role,
            "content": message.parts[0].text
        })

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(session_data, file, indent=4)

    print(f"\nSession saved: {filename}")


def open_past_session():
    if not os.path.exists("sessions"):
        print("\nNo past sessions found.")
        return

    session_files = [
        file for file in os.listdir("sessions")
        if file.endswith(".json")
    ]

    if not session_files:
        print("\nNo past sessions found.")
        return

    print("\nPAST SESSIONS")
    print("=============")

    for index, file in enumerate(session_files, start=1):
        print(f"{index}. {file}")

    try:
        choice = int(input("\nChoose a session: "))

        if choice < 1 or choice > len(session_files):
            print("Invalid session choice.")
            return

        filename = session_files[choice - 1]
        filepath = os.path.join("sessions", filename)

        with open(filepath, "r", encoding="utf-8") as file:
            session_data = json.load(file)

        print("\n================================")
        print("          PAST SESSION")
        print("================================")

        print(f"\nDate: {session_data['date']}")
        print(f"Time: {session_data['time']}")

        print("\n--- CONVERSATION ---")

        for message in session_data["conversation"]:
            if message["role"] == "user":
                print(f"\nYou: {message['content']}")
            else:
                ai_data = validate_ai_response(message["content"])
                print("\nAI:")
                if ai_data is None:
                    print(message["content"])
                else:
                    print_ai_response(ai_data)

        print("\n--- SESSION SUMMARY ---")

        if "summary" not in session_data:
            print("\nNo summary available for this session.")
        else:
            print_session_summary(session_data["summary"])

    except (ValueError, FileNotFoundError, json.JSONDecodeError, KeyError):
        print("\nError: Could not open the selected session.")


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

            if not user_message.strip():
                print("Please enter a message.")
                continue

            if user_message.lower() == "exit":
                if not conversation_history:
                    summary_data = {
                        "summary": "No conversation took place during this session.",
                        "key_stock_issues": [],
                        "recommended_actions": []
                    }
                else:
                    summary_data = generate_session_summary(conversation_history)

                print("\nSESSION SUMMARY:")
                print_session_summary(summary_data)

                save_session(conversation_history, summary_data)

                print("Leaving session...")
                break

            conversation_history.append(
                types.Content(
                    role="user",
                    parts=[types.Part.from_text(text=user_message)]
                )
            )

            try:
                response = client.models.generate_content(
                    model="gemini-3.5-flash-lite",
                    contents=conversation_history,
                    config=types.GenerateContentConfig(
                        system_instruction=system_prompt
                    )
                )

            except Exception as e:
                print("\nError: Unable to contact the AI service.")
                print("Please check your internet connection or try again later.")

                conversation_history.pop()
                continue

            ai_message = response.text
            ai_data = validate_ai_response(ai_message)

            if ai_data is None:
                print("Warning: AI returned invalid JSON. Retrying...")

                try:
                    retry_response = client.models.generate_content(
                        model="gemini-3.5-flash-lite",
                        contents=conversation_history,
                        config=types.GenerateContentConfig(
                            system_instruction=system_prompt
                        )
                    )

                except Exception as e:
                    print("\nError: Unable to contact the AI service.")
                    print("Please check your internet connection or try again later.")

                    conversation_history.pop()
                    continue

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

            if wants_raw_json(user_message):
                print(ai_message)
            else:
                print_ai_response(ai_data)

    elif choice == "2":
        open_past_session()

    elif choice == "3":
        print("\nGoodbye!")
        break

    else:
        print("\nInvalid option. Please choose 1, 2, or 3.")