#
#
#  KookBot X: A khl.py-based micro-framework to build your KOOK bot
# 
#  Please check https://github.com/Gennadiyev/KookBotX for license and more.
# 
#

import sys
import importlib
from pathlib import Path
from loguru import logger
import os
import asyncio
from khl import Bot
from typing import Union, Optional

class KookBotX:

    def __init__(self, token: str):
        self.kookbot = Bot(token=token)

    def configure_logger(self, log_path: Optional[Union[str, Path]]=None):
        # Configure logger, you may change the log file path and rotation settings as you like
        log_path = Path(log_path) if log_path is not None else (Path(__file__).parent / "logs")
        log_path.mkdir(parents=True, exist_ok=True)
        logger.add("logs/kookbotx.log", retention="4 weeks", rotation="1 month", level="DEBUG" if os.environ.get("KOOKBOTX_DEBUG") == "1" else "INFO")

    def load_modules(self, module_path: Optional[Union[str, Path]]=None):
        # Load modules
        module_path = Path(module_path) if module_path is not None else (Path(__file__).parent / "modules")
        module_path.mkdir(parents=True, exist_ok=True)
        # Append to sys.path to make sure the modules can be imported
        sys.path.append(str(module_path))
        # Module could be a singleton .py file, or a folder containing __init__.py and other .py files
        # For each module, import it via invoking the init() function with bot as argument
        bot = self.kookbot
        for module_p in module_path.glob("*"):
            if module_p.is_file() and module_p.suffix == ".py":
                module_name = module_p.stem
                # module = __import__(module_name)
                # module.init(bot)
            elif module_p.is_dir() and (module_p / "__init__.py").exists():
                module_name = module_p.name
            else:
                if module_p.is_dir():
                    logger.warning("Skipping directory {}: no __init__.py found under this directory", module_p)
                else:
                    logger.warning("Skipping file {}: not a .py file", module_p)
                continue
            try:
                module = importlib.import_module(module_name)
            except Exception as e:
                logger.warning("Failed to import module {} ({}): {}", module_name, module_p, e)
                continue
            try:
                _ = module.init(bot)
            except Exception as e:
                logger.warning("Cannot run init() from module {} ({}): {}", module_name, module_p, e)
                continue
            logger.info("Imported module {} from {}", module_name, module_p)
    
    async def start(self):
        assert not hasattr(self, "kookbot_task"), "KookBotX is already running"
        logger.success("KookBotX is starting up!")
        self.kookbot_task = asyncio.create_task(self.kookbot.start())
        await asyncio.wait([self.kookbot_task])

if __name__ == "__main__":
    # Load token from environment variable
    if not os.environ.get("KOOKBOT_WS_TOKEN"):
        logger.error("KOOKBOT_WS_TOKEN is required but not found as an environment variable, exiting...")
        logger.debug("To set the token, either run `export KOOKBOT_WS_TOKEN=your_token`, or invoke this script with `KOOKBOT_WS_TOKEN=your_token python3 {}`", __file__)
        sys.exit(1)
    token = os.environ.get("KOOKBOT_WS_TOKEN")
    # Create KookBotX instance
    kookbotx = KookBotX(token)
    kookbotx.configure_logger()
    kookbotx.load_modules()
    # Start KookBotX
    loop = asyncio.get_event_loop()
    loop.run_until_complete(kookbotx.start())
    loop.close()

