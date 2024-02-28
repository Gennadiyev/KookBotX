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
| Gemini | `gemini-pro` | [Docs](https://ai.google.dev/docs) |
| Zhipu AI | `glm-4` | [Official Website](https://open.bigmodel.cn/) |
| [InternLM](https://github.com/InternLM/InternLM/tree/main) via [LMDeploy](https://github.com/InternLM/LMDeploy)\* | `internlm2-7B` | Accessible after deployment |

\* *InternLM requires self-hosted deployment. A 12 GB VRAM graphics card is required to inference a 7B model without quantization. [Learn more](https://github.com/InternLM/InternLM?tab=readme-ov-file#model-zoo)*

## Proxy Setup

These environment variables will be respected, in a descending order of priority:

- `KOOKBOTX_PROXY`
- `ALL_PROXY`
- `all_proxy`
- `HTTP_PROXY`
- `http_proxy`

