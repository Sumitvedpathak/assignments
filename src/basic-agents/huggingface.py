from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os

load_dotenv()

huggingface_api_key = os.getenv("huggingface_api_key")

client = InferenceClient(api_key=huggingface_api_key)

response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[{"role": "user", "content": "Hello, how are you?"}]
)

print(response.choices[0].message.content)

