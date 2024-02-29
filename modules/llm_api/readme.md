> [!WARNING]
> Generative AI can produce harmful content. Always use it responsibly and consider the potential consequences of your actions.

# LLM-API Module

*Interacting with large language models (LLM) is so much fun!*

> [!IMPORTANT]
> Since this field is evolving rapidly, when you install these libraries it is highly likely that the version numbers and specific APIs will have changed. Please refer to the official documentation for the most up-to-date information.

## Supported Models, Services and Agents

### Models and their Providers

| Provider | Model (in example) | Documentation |
| --- | --- | --- |
| OpenAI | `gpt-4-turbo-preview` | [Docs](https://platform.openai.com/docs/) |
| Gemini (WIP) | `gemini-pro` | [Docs](https://ai.google.dev/docs) |
| Zhipu AI (WIP) | `glm-4` | [Official Website](https://open.bigmodel.cn/) |
| [InternLM](https://github.com/InternLM/InternLM/tree/main) via [LMDeploy](https://github.com/InternLM/LMDeploy)\* (WIP) | `internlm2-7B` | Accessible after deployment |

\* *InternLM requires self-hosted deployment. A 12 GB VRAM graphics card is required to inference a 7B model without quantization. [Learn more](https://github.com/InternLM/InternLM?tab=readme-ov-file#model-zoo)*

## Configuration

Since we are expecting lots of API keys for LLM configuration, we are using a JSON file to store them. The file is expected to be located at `modules/llm_api/config.json`.

Please refer to the `config.json.template` file for the expected structure of the configuration file - that file should be self-explanatory.

### Proxy Setup

Internally, the `proxy` has a pretty complicated logic. In spite of being part of a `config.json` entry, there are also other co-existing environment variables that can be used to set the proxy. In a descending order of priority:

- (Definitely use this one) `proxy` key defined for the specific model in `config.json`
- `proxy` key defined in `config.json`
- `KOOKBOTX_PROXY`
- `ALL_PROXY`
- `all_proxy`
- `HTTP_PROXY`
- (Last resort) `http_proxy`

### Developing new LLMs

A `ConfigLoader` class is used to handle the configuration file, and when you create your own LLMs, you may want to use this class to load your configuration.

Suppose you registered a new LLM class with name `bert-beats-gpt`. Your configuration entry should look like this:

```json
{
    "bert-beats-gpt": {
        "some": "configuration"
    }
}
```

To load your configuration, simply call the `get_config` function:

```python
from .config_loader import get_config

config: dict = get_config("bert-beats-gpt")  # {"some": "configuration"}
```

Note that the proxy will be automatically handled by the `ConfigLoader` class. In other words, it is still handled in the priority order mentioned [above](#proxy-setup).

