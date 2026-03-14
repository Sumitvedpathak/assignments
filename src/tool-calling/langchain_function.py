from langchain.tools import tool, ToolRuntime
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import os
load_dotenv()

@tool("weather_forecast",
description="Returns the weather forecast for a given city. Use this to get the weather of a city.")
def weather_forecast(city: str) -> str:
    """Returns the weather forecast for a given city.
    Args:
        city: The city for which to get the weather forecast.
    Returns:
        The weather forecast for the given city.
    """
    print(f"Getting weather forecast for {city}")
    
    # return f"Its sunny and 20 degrees Celsius."
    return {"temperature": 25, "unit": "celsius"} #Requies json response in case of sequencial function calls.


@tool("set_thermostat_temperature",description="Sets the thermostat temperature. Use this to set the thermostat temperature.")
def set_thermostat_temperature(temperature: int) -> str:
    """
    This function is used to set the thermostat temperature.
    Args:
        temperature: The temperature to set the thermostat to.
    Returns:
        The confirmation that the thermostat temperature has been set.
    """
    print(f"Setting thermostat temperature to {temperature}")
    #return ""
    return {"success": True} ##Requies json response in case of sequencial function calls.


model = init_chat_model("gpt-5-mini", api_key=os.getenv("openai_api_key"))
agent = create_agent(
    model=model,
    tools=[weather_forecast, set_thermostat_temperature],
    system_prompt="You are a helpful assistant that can answer questions and help with tasks."
)

response = agent.invoke(
    {"messages": [{"role": "user", "content": "Set the thermostat temperature to 20 degrees Celsius if it is warmer than 25 else set 18 in Toronto."}]}
)

messages = response.get("messages", [])
if messages:
    print(messages[-1].content)
else:
    print(response)

