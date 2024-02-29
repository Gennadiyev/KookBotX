"""llm_api

Please refer to modules/llm_api/readme.md for more information.
"""

from loguru import logger

from khl import Bot, Event, Message
from khl.api import Message as MessageAPI

from .llm_base import LLM, LLMReturnChunk
from .openai_api import GPT4
import os

DEBUG_FLAG = os.environ.get("KOOKBOTX_DEBUG") == "1"

llm_GPT4 = GPT4()


class LLMStopGeneration(Exception):
    pass


async def call_llm(
    bot: Bot, msg: Message, llm: LLM, command: str, update_per_modification: int = 5
):
    prompt = msg.content[len(command) :].strip()
    if prompt == "":
        await msg.reply("Please provide a prompt for the LLM.")
        return


    try:
        await msg.add_reaction("☕")
        ret = await msg.reply(f"Querying `{llm.name}`...")
        msg_id = ret["msg_id"]
        gate = msg.gate
        response_text = ""
        modifications = 0

        async for chunk in llm.query(prompt):
            if chunk.has_error:
                raise Exception(chunk.error_info)
                break
            if chunk.should_stop:
                raise LLMStopGeneration(chunk.stop_reason)
            response_text += chunk.content
            modifications += 1
            if modifications % update_per_modification == 0:
                if response_text.strip() != "":
                    await gate.exec_req(
                        MessageAPI.update(msg_id=msg_id, content=response_text.strip())
                    )
    except LLMStopGeneration as e:
        if response_text.strip() != "":
            await gate.exec_req(
                MessageAPI.update(msg_id=msg_id, content=response_text.strip())
            )
        else:
            await msg.reply("(No response from the LLM.)")
        await msg.delete_reaction("☕")
        await msg.add_reaction("✅")
        return
    except Exception as e:
        await msg.delete_reaction("☕")
        await msg.add_reaction("❌")
        logger.warning(
            "Error caught when processing command {} (LLM: {})",
            command,
            llm.name if hasattr(llm, "name") else llm,
        )
        logger.warning("{}: {}", e.__class__.__name__, e)
        if DEBUG_FLAG:
            logger.exception(
                "Error caught when processing command {} (LLM: {})",
                command,
                llm.name if hasattr(llm, "name") else llm,
            )
        return


def init(_bot: Bot):

    @_bot.command("gpt")
    async def gpt_4(msg: Message, *args):
        await call_llm(_bot, msg, llm_GPT4, command="/gpt")
