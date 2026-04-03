import os
from langgraph.graph import  START, StateGraph,START, END
from typing import Annotated, TypedDict
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint


# load env
load_dotenv() # Loads variables from .env
os.environ["HUGGINGFACEHUB_API_TOKEN"]



# uising hugging face endpoint
llm = HuggingFaceEndpoint(
    repo_id="meta-llama/Meta-Llama-3-8B-Instruct",
    task="text-generation",
    max_new_tokens=512,
    do_sample=False,
    repetition_penalty=1.03,
    provider="auto",  # let Hugging Face choose the best provider for you
)

chat_model = ChatHuggingFace(llm=llm)


# Define LLMState

class LLMState(TypedDict):
    query: str
    response: str



# define node
def llm_response(state: LLMState)-> LLMState:
    query =  state['query']
    
    prompt = f"""You are a helpful assistant. Please answer the following question: {query}
    """
    
    response = chat_model.invoke(prompt)
    state["response"] =  response.content
    return state




# build workflow
agent_builder  = StateGraph(LLMState)
# add nodes
agent_builder.add_node('llm_response', llm_response)
# add edges to connet the nodes
agent_builder.add_edge(START, 'llm_response')
agent_builder.add_edge("llm_response",END)
# compile the agent
agent = agent_builder.compile()
# Invoke
response = agent.invoke({"query": "what is ai stands for?"})
print(response)