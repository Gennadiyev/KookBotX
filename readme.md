# KookBot X

*Developing KOOK bots with Python made easy*

## Features

- **Simple & easy-to-maintain project structure.** While you still get your working hello world function in 4 lines, scaling up is much easier.

```python
def init(_bot: Bot):
    @_bot.command(name="hello")
    async def hello_world(msg, *args):
        await msg.reply("... world!")
```

- **Lots of examples** to help you get started, including a wide range of applications from LLMs to music streaming and from file serving to currency systems.
- **Easy to use and maintain.** The framework is designed to be easy to use and maintain. You can never get lost in your codebase.

## Quick Start

### Prerequisites

Python 3.9 or higher is required to run this framework. The project is developed and tested on Python 3.9.2, but it should work on any Python 3.9+ version.

Run the following command to install the required packages:

```bash
pip install -r requirements.txt
```

> [!WARNING]  
> Please note: KookBot X uses a customized version of khl.py. We've made modifications to the library and are not affiliated with its original author. For issues related to this customized version, please do not contact the original author of khl.py.

### Running the bot

On Linux, simply run:

```bash
KOOKBOT_WS_TOKEN='<REPLACE_WITH_YOUR_BOT_TOKEN>' python3 main.py
```

On Windows, run:

```powershell
$env:KOOKBOT_WS_TOKEN='<REPLACE_WITH_YOUR_BOT_TOKEN>'; python main.py
```

> [!INFO]
> Make sure to replace `<REPLACE_WITH_YOUR_BOT_TOKEN>` with your own bot token. Grab a token from [KOOK developer platform](https://developer.kookapp.cn/bot). Never share your bot token with anyone. It's like a password to your bot.

If you see a success message, congratulations! You have successfully set up your bot. Now send some message to a shared channel with your bot to see it in action.

Set `KOOKBOTX_DEBUG=1` to see debug messages logged to the log file (default: `logs/kookbotx.log`).

### Database setup (coming soon)

Database integration is planned in future updates.

<!-- ~~Several example modules use databases to store data. We recommend using SQLite for development and PostgreSQL for production.~~ No examples use databases at the moment. -->

## Contributing

We welcome contributions from the community, whether it's some improvements to code structure, a utility module, or more examples. Please read the [contributing guide](#CONTRIBUTING.md) to get started.

### Credits

![Contributors](https://contrib.rocks/image?repo=Gennadiyev/KookBotX)
