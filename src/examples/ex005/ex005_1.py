from typing import List
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langchain_core.tools import BaseTool, tool
from langchain.chat_models import init_chat_model
from rich import print

#1 criar as ferramentas

@tool
def multiply(a:float, b:float) -> float:
    """Multiplica dois números"""
    return a * b


llm = init_chat_model('google_genai:gemini-2.5-flash')


system_message = SystemMessage('You are a helpful assistant. You have access to tools. When the user asks for something, first look if you have the tool to answer the question and solves that problem. ')

human_message = HumanMessage("Oi, sou o Tiago Sousa. Multiplique 2 por 3")
messages: List[BaseMessage] = [system_message, human_message]


tools: List[BaseTool] = [multiply]
llm_with_tools = llm.bind_tools(tools)

result = llm_with_tools.invoke(messages)
print(result)
