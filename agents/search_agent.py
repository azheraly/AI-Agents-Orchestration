from langchain.agents import create_agent
from dotenv import load_dotenv
import os
from langchain_tavily import TavilySearch
from langchain_groq import ChatGroq

load_dotenv()


llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=1,
    reasoning_format="parsed",
)


def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's dark cloudy in {city}!"


search_tool = TavilySearch(
    api_key=os.environ.get("TAVILY_API_KEY"),
    topic="general",
    max_results=3,
)

agent = create_agent(
    model=llm, tools=[search_tool], system_prompt="You are a helpful assistant"
)


result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "what is the weather in Islamabad Pakistan today?",
            }
        ]
    }
)


print(result["messages"][-1].content_blocks)

# result = search_tool.invoke({"query": "give me the latest news on ai?"})
# print(result["results"])


