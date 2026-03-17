from contextlib import asynccontextmanager, contextmanager
from typing import AsyncGenerator, Generator
from langchain.chat_models import BaseChatModel, init_chat_model
from functools import lru_cache
def load_llm() -> BaseChatModel:
    return init_chat_model("google_genai:gemini-2.5-flash")





class Connection:
    def use(self) -> None:
        print("using connection")
    def open_connection(self) -> None:
        print("connection opened")
    def close_connection(self) -> None:
        print("connection closed")

@lru_cache(maxsize=1)
def get_connection() -> Connection:
    return Connection()

@contextmanager
def sync_lifespan() -> Generator[Connection]:
    print("Abri")
    yield get_connection()
    print("Fechei")

@asynccontextmanager
async def async_lifespan() -> AsyncGenerator[Connection]:
    print("Abri")
    yield get_connection()
    print("Fechei")
