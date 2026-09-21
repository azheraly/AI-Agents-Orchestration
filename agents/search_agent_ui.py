import streamlit as st
from langchain.agents import create_agent
from dotenv import load_dotenv
import os
from langchain_tavily import TavilySearch
from langchain_groq import ChatGroq
from langchain.tools import tool
import requests

load_dotenv()

st.set_page_config(page_title="AI Agent Chat", page_icon="🤖", layout="centered")
st.title("🤖 AI Agent Chat")
st.caption("Powered by Groq · Tavily Search · Weatherstack")


@st.cache_resource
def build_agent():
    """Build the agent once and cache it."""
    llm = ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=1,
        reasoning_format="parsed",
    )

    @tool
    def get_weather(city: str) -> str:
        """Get weather for a given city."""
        response = requests.get(
            f"http://api.weatherstack.com/current"
            f"?access_key={os.environ.get('WEATHERSTACK_API_KEY')}&query={city}"
        )
        data = response.json()
        if "current" not in data:
            return f"Could not retrieve weather data for {city}. Please check the city name and try again."
        temperature = data["current"]["temperature"]
        weather_descriptions = data["current"]["weather_descriptions"]
        return (
            f"The current temperature in {city} is {temperature}°C "
            f"with {', '.join(weather_descriptions)}."
        )

    search_tool = TavilySearch(
        api_key=os.environ.get("TAVILY_API_KEY"),
        topic="general",
        max_results=3,
    )

    return create_agent(
        model=llm,
        tools=[search_tool, get_weather],
        system_prompt="You are a helpful assistant",
    )


agent = build_agent()

# ---- Chat history (kept in session state so it survives reruns) ----
if "messages" not in st.session_state:
    st.session_state.messages = []

# Render previous turns
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---- Input ----
if prompt := st.chat_input("Ask me anything — e.g. 'what is the weather in Islamabad?'"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_text = ""

        # Stream the agent's response token by token
        for chunk, metadata in agent.stream(
            {"messages": [{"role": "user", "content": prompt}]},
            stream_mode="messages",
        ):
            if chunk.content:
                full_text += chunk.content
                placeholder.markdown(full_text + "▌")
        placeholder.markdown(full_text)

    st.session_state.messages.append({"role": "assistant", "content": full_text})

# ---- Sidebar extras ----
with st.sidebar:
    st.header("About")
    st.write(
        "This agent can:\n"
        "- 🔍 Search the web (Tavily)\n"
        "- 🌦️ Get live weather (Weatherstack)"
    )
    if st.button("Clear chat"):
        st.session_state.messages = []
        st.rerun()