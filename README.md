# Comparing Insurance Quotes using Azure OpenAI

Use AI to compare insurance, or other financial quotes.

> Default system messages assume insurance quotes. Update them for your use-case.

## Features

1. Compare different quotes
2. Try different OpenAI models.
3. Try different system messages and user promprts.
4. Add and update system messages
5. Add and update user prompts
6. Manage completion history

![screenshot](./diagrams/screenshot.png)

## Quick Start (commands for git bash on Windows)

### 1. Create `.env` file locally

Create a new file `.env` with API keys and region details from Azure AI Speech to Text service.

```.env
AZURE_OPENAI_ENDPOINT=<>
AZURE_OPENAI_API_KEY=<>
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o-mini
```

Optional - if you want to try out other models. You can add additional model details to your `.env` file.

Instructions:

<details>

```
## Additional model configurations
# o3 mini
MODEL_O3_MINI_NAME=o3-mini
MODEL_O3_MINI_ENDPOINT=<>
MODEL_O3_MINI_API_KEY=<>
MODEL_O3_MINI_DEPLOYMENT_NAME=o3-mini
MODEL_O3_MINI_API_VERSION=2024-12-01-preview
MODEL_O3_MINI_TOKEN_PARAM=max_completion_tokens # o3 mini uses max_completion_token as parameter name
MODEL_O3_MINI_UNSUPPORTED_PARAMS=temperature # o3 mini does not support temperature

# 4o
MODEL_4O_NAME=4o
MODEL_4O_ENDPOINT=<>
MODEL_4O_API_KEY=<>
MODEL_4O_DEPLOYMENT_NAME=4o
MODEL_4O_API_VERSION=2025-01-01-preview
MODEL_4O_TOKEN_PARAM=max_tokens
```
</details>

### 2. Install

`python -m venv .venv`

`source .venv/Scripts/activate`

`pip install -r requirements.txt -r requirements-dev.txt`

### 3. Notebook

Review [chat-completion.ipynb](./notebooks/chat-completion.ipynb).

Or skip directly to next part.

### 4. Run Demo

`python -m streamlit run app.py`

### 5. Explore the demo

[http://localhost:8501/](http://localhost:8501/)

[Demo Video](./diagrams/demo.mp4)



https://github.com/user-attachments/assets/2bdb28d9-eb2d-42b4-a1e5-a6c7e3074831



## Contributing (Committing changes)




Install pre-commit for basic checks and fixes before commit.

`pre-commit install`
