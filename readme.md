# KookBot X

*Developing KOOK bots with Python made easy*

## Features

- **Simple yet easy-to-maintain project structure.** While you still get your working hello world function in 4 lines, scaling up is much easier.

```python
def init(_bot: Bot):
    @_bot.command(name="hello")
    async def dice(msg, *args):
        await msg.reply("... world!")
```

- **Lots of examples** for you to get started, ranging from a plethora of LLMs to music streaming, from file serving to a currency system.
- **Easy to use and maintain.** The framework is designed to be easy to use and maintain. You can never get lost in your codebase.

## Quick Start

### Prerequisites

Python 3.10 or higher is required to run this framework.

Run the following command to install the required packages:

```bash
pip install -r requirements.txt
```

> [!WARNING]  
> KookBotX is built upon a customized `khl.py` - we modified some code in the library. We are not associated with the original author of `khl.py`. If you use this version of `khl.py`, please refrain from contacting the original author of khl.py with issues related to this modified version.

### Running the bot

On Linux, run:

```
TOKEN=<REPLACE_WITH_YOUR_BOT_TOKEN> python3 main.py
```

## Contributing

We welcome contributions from the community, whether it's some improvements to code structure, a utility module, or more examples. Please read the [contributing guide](#) to get started.

### Credits

![Contributors](https://contrib.rocks/image?repo=Gennadiyev/KookBotX)
