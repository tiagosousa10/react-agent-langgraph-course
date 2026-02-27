from langchain.tools import BaseTool, tool


@tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers together."""
    return a * b

@tool
def sum_numbers(a: float, b: float) -> float:
    """Sum two numbers together."""
    return a * b

@tool
def subtract_numbers(a: float, b: float) -> float:
    """Subtract two numbers together."""
    return a - b

@tool
def divide_numbers(a: float, b: float) -> float:
    """Divide two numbers together."""
    return a / b

TOOLS: list[BaseTool] = [multiply, sum_numbers, subtract_numbers, divide_numbers]
TOOLS_BY_NAME: dict[str, BaseTool] = {tool.name: tool for tool in TOOLS}
