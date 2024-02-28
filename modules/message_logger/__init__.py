'''message_logger

Message logger does a simple job: log incoming messages to the console. Many fields of khl.py instances are used in this module (e.g. Guild, GuildUser), so it's a good example of how to use khl.py classes.
'''


import os
from khl import EventTypes, Bot, Event, Message
from loguru import logger

def init(bot_):
    
    @bot_.on_message()
    async def message_logger(m: Message):
        if os.environ.get("KOOKBOTX_DEBUG") == "1":
            logger.debug("Message #{mid} inbounds | from user {nickname} = {username} (#{uid}) {is_bot} | from channel {channel_name} (#{cid}), guild #{gid} | Content: {content}", mid=m.id, nickname=m.author.nickname, username=m.author.username, uid=m.author.id, is_bot="[BOT]" if m.author.bot else "[ONLINE]" if m.author.online else "[OFFLINE]", channel_name=m.channel.name, cid=m.channel.id, gid=m.guild.id, content=m.content)
        logger.opt(colors=True).info("<- [<cyan>{nick}</cyan>] {content}", nick=m.author.nickname, content=m.content)
