#
# OpenAI (https://platform.openai.com/)
#

try:
    import openai
    from openai import AsyncOpenAI
except ImportError:
    logger.warning(
        "OpenAI module not found or you are using a version without critical client API. Please install it via `pip install openai==1.12.0`"
    )

import asyncio
from typing import AsyncIterator

from httpx import AsyncClient
from loguru import logger

from .llm_base import LLM, LLMReturnChunk


class GPT4(LLM):
    def __init__(self):
        super().__init__(
            "gpt-4"
        )  # self.config should be populated with the corresponding configuration
        self.build_client()

    def build_client(self):
        """Build httpx client for OpenAI API. If a proxy is provided (e.g. http://127.0.0.1:25501), it will be used."""
        proxy = self.config.get("proxy", None)
        api_key = self.config.get("api_key", None)
        if api_key is None:
            logger.warning(
                "OpenAI API key not found. Please set it in the config file."
            )
            self.client = None
            return
        if proxy:
            httpx_client = AsyncClient(proxies=proxy)
            self.client = AsyncOpenAI(
                api_key=api_key, http_client=httpx_client
            )
        else:
            self.client = AsyncOpenAI(api_key=self.config["api_key"])

    async def query(self, query_str: str) -> AsyncIterator[LLMReturnChunk]:
        """Query GPT-4 with the given query string, streaming the response back in chunks."""
        if self.client is None:
            yield LLMReturnChunk(
                has_error=True,
                error_info="OpenAI client is not available. Please refer to the logs for more information.",
                content="An error occurred.",
            )
            return
        # Simulating sending a query to GPT-4 and receiving streamed responses
        response = await self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[{"role": "user", "content": query_str}],
            temperature=0.3,
            stream=True,
        )

        async for chunk in response:
            try:
                # Assuming chunk structure has 'choices' with 'finish_reason' and 'delta' with 'content'
                should_finish = chunk.choices[0].finish_reason
                try:
                    delta_content = chunk.choices[0].delta.content
                except AttributeError:
                    delta_content = ""

                if should_finish:
                    # If should_finish is a stop reason, send a final chunk and break
                    yield LLMReturnChunk(
                        should_stop=True,
                        content=delta_content,
                        stop_reason=should_finish
                    )
                    break
                else:
                    # Otherwise, send the content chunk and continue
                    yield LLMReturnChunk(
                        should_stop=False, content=delta_content
                    )

            except Exception as e:
                # Handle any exceptions by sending an error chunk
                yield LLMReturnChunk(
                    should_stop=True, has_error=True, error_info=str(e), content="An error occurred."
                )
                break
