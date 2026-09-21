from langchain.agents import create_agent
from dotenv import load_dotenv
import os
from langchain_tavily import TavilySearch
from langchain_groq import ChatGroq
from langchain.tools import tool
import requests

load_dotenv()


llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=1,
    reasoning_format="parsed",
)


@tool
def get_weather(city: str) -> str:
    """Get weather for a given city."""

    response = requests.get(
        f"http://api.weatherstack.com/current?access_key={os.environ.get('WEATHERSTACK_API_KEY')}&query={city}"
    )
    data = response.json()
    if "current" not in data:
        return f"Could not retrieve weather data for {city}. Please check the city name and try again."
    else:
        temperature = data["current"]["temperature"]
        weather_descriptions = data["current"]["weather_descriptions"]
        return f"The current temperature in {city} is {temperature}°C with {', '.join(weather_descriptions)}."


search_tool = TavilySearch(
    api_key=os.environ.get("TAVILY_API_KEY"),
    topic="general",
    max_results=3,
)

agent = create_agent(
    model=llm,
    tools=[search_tool, get_weather],
    system_prompt="You are a helpful assistant",
)


result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "what is the weather in Islamabad Pakistan today?",
            }
        ]
    },
)


print(result["messages"][-1].content_blocks)
