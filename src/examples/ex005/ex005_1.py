from typing import List
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_core.tools import BaseTool, tool
from langchain.chat_models import init_chat_model
from pydantic import ValidationError
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
tools_by_name = {tool.name: tool for tool in tools}
llm_with_tools = llm.bind_tools(tools)

llm_response = llm_with_tools.invoke(messages)
messages.append(llm_response)

if isinstance(llm_response, AIMessage) and getattr(llm_response, "tool_calls", None):
    call = llm_response.tool_calls[-1]
    name, args, id_ = call["name"], call["args"], call["id"]

    try:
        content = tools_by_name[name].invoke(args)
        status = "success"
    except (KeyError, IndexError, TypeError, ValidationError, ValueError) as error:
        content = f"Please, fix your mistakes: {error}"
        status = "error"


    llm_response = llm_with_tools.invoke(messages)
    messages.append(llm_response)


print(messages)
