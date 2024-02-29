from pathlib import Path
from typing import Union

from loguru import logger
import orjson
import os


DEBUG_FLAG = os.environ.get("KOOKBOTX_DEBUG") == "1"


class ConfigLoader:
    def __init__(self, config_file: Union[Path, str] = None):
        self.config_file = (
            Path(config_file) if config_file else Path(__file__).parent / "config.json"
        )
        logger.debug("Loading LLM config file from {}", self.config_file.resolve())
        self.config = {}
        try:
            self.load_config()
        except orjson.JSONDecodeError:
            logger.warning(
                "Error loading LLM config file, please check your JSON formatting"
            )
            self.config = {}
        except Exception as e:
            if DEBUG_FLAG:
                logger.exception("Error loading LLM config file, {}", e)
            else:
                logger.warning("Error loading LLM config file: {}", e)
            self.config = {}

    def load_config(self):
        with open(self.config_file, "rb") as f:
            self.config = orjson.loads(f.read())
        self.default_proxy = (
            self.config.get("proxy", False)
            or os.environ.get("KOOKBOTX_PROXY")
            or os.environ.get("ALL_PROXY")
            or os.environ.get("all_proxy")
            or os.environ.get("HTTP_PROXY")
            or os.environ.get("http_proxy")
            or None
        )

    def get_config(self, key: str, default=None):
        """Note: If default is set, no proxy change will be made"""
        if key == "proxy":
            return self.default_proxy
        conf = self.config.get(key, default)
        if conf is None:
            return default
        conf_copy: dict = conf.copy()
        if self.default_proxy is not None and "proxy" not in conf_copy:
            conf_copy["proxy"] = self.default_proxy
        return conf_copy


default_config_loader = ConfigLoader()


def get_config(key: str):
    return default_config_loader.get_config(key)
