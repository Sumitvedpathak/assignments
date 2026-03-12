from google import genai
from google.genai import types
import dotenv
import os

dotenv.load_dotenv()

# Gemini source doc - https://ai.google.dev/gemini-api/docs/function-calling?example=weather

# Function declaration for the weather forecast tool for manual tool calling
weather_forecast_declaration = {
    "name": "weather_forecast",
    "description": "Get the weather forecast for a given city",
    "parameters": {
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "The city for which to get the weather forecast."
            }
        },
        "required": ["city"]
    }
}

# Function to use gemini as tool calling agent with manual tool calling
def get_gemini_client_Manual_ToolCalling(user_prompt: str):
    gemini_api_key = os.getenv("gemini_api_key")
    client = genai.Client(api_key=gemini_api_key)
    # Step 1: Set up the tools declaration
    tools = types.Tool(function_declarations=[weather_forecast_declaration])
    # Step 2: Set up the configuration
    config = types.GenerateContentConfig(tools=[tools])
    # Step 3: Set up the contents
    contents = []
    contents.append(types.Content(role="user", parts=[types.Part(text=user_prompt)]))
    # Step 4: Call LLM to get the response
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=contents,
        config=config
    )
    print("Response: ", response)
    # Step 5: Check if the response contains a function call
    if response.candidates[0].content.parts[0].function_call:
        function_call = response.candidates[0].content.parts[0].function_call
        print("Function call: ", function_call.name)
        print("Function call args: ", function_call.args)
        # Step 6: Call the function with the arguments
        result = weather_forecast(function_call.args["city"])
        print("Result: ", result)
        # Step 7: Set up the function response part
        function_response_part = types.Part.from_function_response(
            name=function_call.name,
            response={"result": result}
        )
        # Step 8: Add the function response part to the contents
        contents.append(response.candidates[0].content)
        # Step 9: Add the user content to the contents
        contents.append(types.Content(role="user", parts=[function_response_part]))
        # Step 10: Call LLM to get the final response
        final_response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents,
            config=config
        )
        print("Final response: ", final_response)
        return final_response.text

# Function to use gemini as tool calling agent with auto tool calling - phyton only
def get_gemini_client_Auto_ToolCalling(user_prompt: str):
    gemini_api_key = os.getenv("gemini_api_key")
    client = genai.Client(api_key=gemini_api_key)
    # Step 2: Set up the configuration
    config = types.GenerateContentConfig(tools=[weather_forecast])
    # Step 3: Set up the contents
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_prompt,
        config=config
    )
    # print("Response: ", response)
    return response.text
    
    # Function to use gemini as tool calling agent with auto tool calling - sequence of function calls
def get_gemini_client_Auto_ToolCalling_seq_function_calls(user_prompt: str):
    gemini_api_key = os.getenv("gemini_api_key")
    client = genai.Client(api_key=gemini_api_key)
    # Step 2: Set up the configuration
    config = types.GenerateContentConfig(tools=[set_thermostat_temperature, weather_forecast])
    # Step 3: Set up the contents
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_prompt,
        config=config
    )
    # print("Response: ", response)
    return response.text

def weather_forecast(city: str) -> str:
    """
    This function is used to get the weather forecast for a given city.
    Args:
        city: The city for which to get the weather forecast.
    Returns:
        The weather forecast for the given city.
    """
    print(f"Getting weather forecast for {city}")
    # return f"Its sunny and 20 degrees Celsius."
    return {"temperature": 25, "unit": "celsius"} #Requies json response in case of sequencial function calls.

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

# tools = [weather_forecast]

if __name__ == "__main__":
    user_prompt = input("Enter your prompt: ")
    # print(get_gemini_client_Manual_ToolCalling(user_prompt))
    # print(get_gemini_client_Auto_ToolCalling(user_prompt))
    print(get_gemini_client_Auto_ToolCalling_seq_function_calls(user_prompt))






