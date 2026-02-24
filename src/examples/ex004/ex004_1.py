from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import Messages
from rich import print

from langgraph.graph import START,END, StateGraph, add_messages

def reducer(a: Messages,b:Messages) -> Messages:
    print("> reducer em execução", f"{a=}", f"{b=}")
    return add_messages(a,b)

# 1 - Defino o estado
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage],reducer]


# 2 - Defino os meus nodes
def call_llm(state:AgentState) :
    return None

#Crio o state graph
builder = StateGraph(AgentState, context_schema=None, input_schema=AgentState, output_schema=AgentState)

# 4- adicono nodes ao grafo
builder.add_node("call_llm", call_llm)
builder.add_edge(START, "call_llm")
builder.add_edge("call_llm", END)

# 5 - Compilo o grafo
graph = builder.compile()

if __name__ == "__main__":
    result = graph.invoke({'messages': []})
    print(result)
