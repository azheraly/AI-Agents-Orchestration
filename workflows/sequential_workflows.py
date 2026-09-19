from langgraph.graph import  START, StateGraph,START, END
from typing import Annotated, TypedDict


# Define State

class State(TypedDict):
    height: float
    weight: float
    bmi: float

# define node
def calculate_bmi(state: State)-> State:
    weight =  state['weight']
    height = state['height']
    
    bmi = weight /(height*2)
    
    state["bmi"] =  bmi
    return state

# build workflow
agent_builder  = StateGraph(State)
# add nodes
agent_builder.add_node('calculate_bmi', calculate_bmi)

# add edges to connet the nodes
agent_builder.add_edge(START, 'calculate_bmi')
agent_builder.add_edge("calculate_bmi",END)

# compile the agent
agent = agent_builder.compile()
# Invoke
print(agent.invoke({'height':20, 'weight':30}))







    

