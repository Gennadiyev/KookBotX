import asyncio
from dataclasses import dataclass
from typing import AsyncIterator

from loguru import logger

from .config_loader import get_config


@dataclass
class LLMReturnChunk:
    # Typcial LLM chunk
    should_stop: bool
    stop_reason: str = ""
    content: str = ""
    # Error handling
    has_error: bool = False
    error_info: str = ""


class LLM:

    def __init__(self, name):
        """Initialize an LLM instance with the given name. The name is used to load the corresponding configuration from the config file. See `config_loader.py` for more information."""
        self.name = name
        self.config = self.get_config(name)

    def get_config(self, name):
        return get_config(name)

    async def query(self, query_str: str) -> AsyncIterator[LLMReturnChunk]:
        """Query an LLM about given query string.

        By default, only streaming LLMs are supported. A typical use case is to use this method in an async context:

        ```python
        async for chunk in llm.query("Hello! Who are you?"):
            if chunk.has_error:
                print("Error:", chunk.content)
                break
            if chunk.should_stop:
                print("\n")
                break
            print(chunk.content)
        ```

        Each chunk is an instance of `LLMReturnChunk`. The `should_stop` field indicates whether the LLM has finished processing the query and the `content` field contains the actual content of the chunk. If `has_error` is `True`, the `error_info` field contains the error message.
        """
        if self.name == "NoModel":
            for i in range(3):
                if i == 0:
                    await asyncio.sleep(0.2)
                    yield LLMReturnChunk(
                        should_stop=False, content="Hello! I am an LLM-API example. "
                    )
                elif i == 1:
                    await asyncio.sleep(0.2)
                    yield LLMReturnChunk(
                        should_stop=False,
                        content="You should implement your own LLM class from here!\n",
                    )
                else:
                    await asyncio.sleep(0.2)
                    yield LLMReturnChunk(should_stop=True, stop_reason="stop")
        else:
            raise NotImplementedError(
                "Please implement your own LLM class from the LLM base class."
            )


async def __test():
    llm = LLM("NoModel")
    async for chunk in llm.query("Hello! Who are you?"):
        if chunk.has_error:
            print("Error:", chunk.content)
            break
        if chunk.should_stop:
            print("STOPPED: {}\n".format(chunk.stop_reason))
            break
        print(chunk.content)


if __name__ == "__main__":
    asyncio.run(__test())
