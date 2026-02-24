from typing import Annotated, TypedDict

from langgraph.graph import END, START, StateGraph
from rich import print




def reducer(a: list[str], b: list[str]) -> list[str]:
    # Aqui você poderia usar operator.add ou add_messages (falaremos adiante)
    reducer_result = a + b
    print("> reducer em execução", f"{reducer_result=}")
    return reducer_result


class State(TypedDict):
    # Meu estado tem um único campo (você pode colocar quantos campos preferir)
    # Se queremos que o estado anterior seja mantido, precisamos de `Annotated`
    # com o tipo deste campo mais uma função de reducer. O trabalho do reducer
    # é receber `a` e `b` (estado anterior e o novo) e unir os dois de alguma
    # forma. Aqui temos a + b (uma lista + outra faz a concatenação de ambas)
    nodes_path: Annotated[list[str], reducer]  # O tipo é list[str]


# A definição dos nodes
# Cada node receberá o estado como input e poderá (ou não) manipular este estado.
def node_a(state: State) -> State:
    final_state: State = {"nodes_path": ["A"]}
    print("> node_a em execução", f"{state=}", f"{final_state=}")
    return final_state  # só estou gerando um novo estado


def node_b(state: State) -> State:
    final_state: State = {"nodes_path": ["B"]}
    print("> node_b em execução", f"{state=}", f"{final_state=}")
    return final_state  # só estou gerando um novo estado


# A definição do construtor do grafo
# O nosso grafo precisará ser construído e depois compilado. Isso garante que
# todos os nós e edges estão conectados corretamente.
print("Criando o StateGraph")
builder = StateGraph(State)

# A adição dos nodes
print("Adicionando os nodes")
builder.add_node("A", node_a)
builder.add_node("B", node_b)

# A ligação dos nodes com edges
print("Conectando as edges")
builder.add_edge(START, "A")
builder.add_edge("A", "B")
builder.add_edge("B", END)

# A compilação do grafo
print("Compilando o grafo...")
graph = builder.compile()

# Por fim, podemos usar o grafo
print()
print("Executando o grafo com `invoke`")
response = graph.invoke({"nodes_path": []})
print()

# O resultado depois de passar em todos os nodes do grafo
print("Aqui está o resultado final...")
print(f"{response=}")
print()
