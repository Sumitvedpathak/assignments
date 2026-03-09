from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

gemini_api_key = os.getenv("gemini_api_key")

client = genai.Client(api_key=gemini_api_key)
conversation_history = []

try:
    while True:
        user_input = input("Enter your prompt: ")
        if user_input == "exit":
            print("Exiting...")
            break

        conversation_history.append(f"User: {user_input}")
        prompt_with_context = (
            "Continue this conversation naturally.\n\n"
            + "\n".join(conversation_history)
            + "\nAssistant:"
        )

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt_with_context,
        )
        assistant_reply = response.text
        print(assistant_reply)
        conversation_history.append(f"Assistant: {assistant_reply}")
except Exception as e:
    print(e)
