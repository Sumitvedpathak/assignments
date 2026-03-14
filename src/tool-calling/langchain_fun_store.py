from typing import Any
from langgraph.store.memory import InMemoryStore
from langchain.agents import create_agent
from langchain.tools import tool, ToolRuntime
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
load_dotenv()


# Access memory
@tool
def get_user_info(user_id: str, runtime: ToolRuntime) -> str:
    """Look up user info."""
    store = runtime.store
    user_info = store.get(("users",), user_id)
    return str(user_info.value) if user_info else "Unknown user"

# Update memory
@tool
def save_user_info(user_id: str, user_info: dict[str, Any], runtime: ToolRuntime) -> str:
    """Save user info."""
    store = runtime.store
    print("Saving user info: ", user_info)
    store.put(("users",), user_id, user_info)
    return "Successfully saved user info."

store = InMemoryStore()
model = ChatOpenAI(model="gpt-5-mini", api_key=os.getenv("openai_api_key"))
agent = create_agent(
    model,
    tools=[get_user_info, save_user_info],
    store=store
)

# First session: save user info
result = agent.invoke({
    "messages": [{"role": "user", "content": "Save the following user: userid: abc123, name: Foo, age: 25, email: foo@langchain.dev"}]
})
messages = result.get("messages", [])
if messages:
    print("First session: ", messages[-1].content)
else:
    print(result)

# Second session: get user info
result = agent.invoke({
    "messages": [{"role": "user", "content": "Get user info for user with id 'abc123'"}]
})
messages = result.get("messages", [])
if messages:
    print("Second session: ", messages[-1].content)
else:
    print(result)
# Here is the user info for user with ID "abc123":
# - Name: Foo
# - Age: 25
# - Email: foo@langchain.dev