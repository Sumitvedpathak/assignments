from langchain.tools import tool

@tool("weather_forecast",description="Returns the weather forecast for a given city. Use this to get the weather of a city.")
def weather_forecast(city: str) -> str:
    """Returns the weather forecast for a given city.
    Args:
        city: The city for which to get the weather forecast.
    Returns:
        The weather forecast for the given city.
    """
    print(f"Getting weather forecast for {city}")
    return f"Its sunny and 20 degrees Celsius."
    # return {"temperature": 25, "unit": "celsius"} #Requies json response in case of sequencial function calls.

