import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

anthropic_api_key = os.getenv("anthropic_api_key")

client = Anthropic(api_key=anthropic_api_key)

messages = []


while True:
    user_input = input("Enter your prompt: ")
    if user_input == "exit":
        print("Exiting...")
        break
    messages.append({
        "role": "user",
        "content": user_input
    })  
    response = client.messages.create(
        system="You are a helpful assistant.",
        max_tokens=100,
        model="claude-haiku-4-5",
        messages=messages
    )
    print(response.content[0].text)
    messages.append({
        "role": "assistant",
        "content": response.content[0].text
    })



