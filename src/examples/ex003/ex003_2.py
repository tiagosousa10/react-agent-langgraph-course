import operator
from dataclasses import dataclass
from typing import Annotated, Literal

from langgraph.graph import END, START, StateGraph
from rich import print

# Este é o mesmo código anterior, só removi os comentários.

# Definições do estado e dos nodes


@dataclass
class State:
    nodes_path: Annotated[list[str], operator.add]  # operator.add = a + b
    # Vamos usar esse current_number para nossa conditional edge
    current_number: float = 0


def node_a(state: State) -> State:
    final_state: State = State(nodes_path=["A"], current_number=state.current_number)
    print("> node_a em execução", f"{state=}", f"{final_state=}")
    return final_state  # só estou gerando um novo estado


def node_b(state: State) -> State:
    final_state: State = State(nodes_path=["B"], current_number=state.current_number)
    print("> node_b em execução", f"{state=}", f"{final_state=}")
    return final_state  # só estou gerando um novo estado


# TEMOS UM NOVO NODE!
def node_c(state: State) -> State:
    final_state: State = State(nodes_path=["C"], current_number=state.current_number)
    print("> node_c em execução", f"{state=}", f"{final_state=}")
    return final_state  # só estou gerando um novo estado



def the_conditions(state: State) -> Literal["goes_to_b", "goes_to_c"]:

    b_max_number = 50
    should_go_to_b = state.current_number <= b_max_number



    if should_go_to_b:
        # Então retornamos o nome da edge para o grafo seguir
        return "goes_to_b"

    # Único outro caminho possível é este
    return "goes_to_c"


# Definição e compilação do grafo

builder = StateGraph(
    State, input_schema=State, context_schema=None, output_schema=State
)

builder.add_node("A", node_a)
builder.add_node("B", node_b)
builder.add_node("C", node_c)  # NOVO NODE!!!


builder.add_edge(START, "A")

builder.add_conditional_edges(
    "A",
    the_conditions,
    {
        "goes_to_b": "B",
        "goes_to_c": "C",
    },
)

# E agora qual nome vai para END? `B` e `C`.
builder.add_edge("B", END)
builder.add_edge("C", END)


graph = builder.compile()

# Execução do código

print()
# 10 deve ir de `A` para `B`
response = graph.invoke(State(nodes_path=[], current_number=10))
print(f"{response=}")
print()
# 51 deve ir de `A` para `C`
response = graph.invoke(State(nodes_path=[], current_number=51))
print(f"{response=}")
print()
