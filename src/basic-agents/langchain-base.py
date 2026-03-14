from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import os
from langchain.messages import AIMessage, SystemMessage, HumanMessage

load_dotenv()
# model = init_chat_model("gpt-4o-mini", api_key=os.getenv("openai_api_key"))
model = init_chat_model("claude-sonnet-4-6", api_key= os.getenv("anthropic_api_key"))
# response = model.invoke("What is the capital of France?")
# print(response.content)




# Create an AI message manually (e.g., for conversation history)
ai_msg = AIMessage("I'd be happy to help you with that question!")

# Add to conversation history
messages = [
    SystemMessage("You are a helpful assistant"),
    HumanMessage("Can you help me?"),
    ai_msg,  # Insert as if it came from the model
    HumanMessage("Great! What's 2+2?")
]

# model = init_chat_model("gpt-5-mini", api_key=os.getenv("openai_api_key"))

response = model.invoke(messages)
print(response.content)