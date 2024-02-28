"""hello_world

Time to fulfill the 4-liner promise. Here's the hello_world module!

For the first function, hello_world, use `/hello` in any channel the bot can see. The bot will reply with "... world!"

For the second function, use `/hi KunBot` in any channel the bot can see. The bot will reply with "Hey there, KunBot!"

Isn't that simple? Now you can see how to use the `@bot.command` decorator to define a command, and how to use `Message.reply` to send a message back to the channel.
"""

from khl import Bot, Event, Message


def init(_bot: Bot):

    @_bot.command(name="hello")
    async def hello_world(msg: Message):
        await msg.reply("... world!")

    @_bot.command(name="hi")
    async def hi_you(msg: Message, *args):
        await msg.reply("Hey there, {}!".format(" ".join(args)))
