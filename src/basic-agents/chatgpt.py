from openai import  OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

openai_api_key = os.getenv("openai_api_key")

client = OpenAI()

response = client.responses.create(
    model="gpt-4o-mini",
    input="Hello, how are you?"
)
print(response.output_text)


response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Hello, how are you?"}]
)
print(response.choices[0].message.content)


# Using the OpenAI API directly. This can be used by changing the base_url to any provider like anthropic, gemini, etc.
OpenAI_base_url="https://api.openai.com/v1"
Anthropic_base_url="https://api.anthropic.com/v1"
Gemini_base_url="https://api.google.com/v1"
ollama_base_url="http://localhost:11434/v1"
huggingface_base_url="https://api.huggingface.co/v1"
openrouter_base_url="https://openrouter.ai/api/v1"

client = OpenAI( api_key=openai_api_key, base_url=OpenAI_base_url)
messages = [{"role": "system", "content": "You are a helpful assistant."}]
while True:
    user_input = input("Enter your prompt: ")
    if user_input == "exit":
        print("Exiting...")
        break
    messages.append({"role": "user", "content": user_input})
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    print(response.choices[0].message.content)
    messages.append({"role": "assistant", "content": response.choices[0].message.content})
