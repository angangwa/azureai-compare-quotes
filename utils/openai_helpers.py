"""Azure OpenAI Helpers"""
import os
import streamlit as st
from openai import AzureOpenAI


def setup_client(model_name=None):
    """
    Set up the Azure OpenAI client using environment variables.
    If model_name is provided, use model-specific credentials.
    """
    try:
        # Use model-specific credentials if provided
        if model_name:
            # Create prefix for model-specific env vars
            prefix = f"MODEL_{model_name.upper().replace('-', '_')}"
            api_key = os.getenv(f"{prefix}_API_KEY")
            endpoint = os.getenv(f"{prefix}_ENDPOINT")
            api_version = os.getenv(f"{prefix}_API_VERSION", "2024-02-15-preview")
        else:
            # Fallback to default credentials
            api_key = os.getenv("AZURE_OPENAI_API_KEY")
            endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
            api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")

        if not api_key or not endpoint:
            st.error(
                f"Missing API key or endpoint for model: {model_name or 'default'}"
            )
            return None

        client = AzureOpenAI(
            api_key=api_key,
            api_version=api_version,
            azure_endpoint=endpoint,
        )
        return client
    except (ValueError, KeyError, RuntimeError) as e:
        st.error(f"Error setting up Azure OpenAI client: {str(e)}")
        return None


def get_completion(
    client,
    deployment_name,
    system_message,
    user_prompt,
    temperature=0.7,
    max_tokens=1000,
    model_name=None,
):
    """Get a completion from the specified model."""
    try:
        # If model_name is provided, use model-specific deployment name and parameters
        if model_name:
            prefix = f"MODEL_{model_name.upper().replace('-', '_')}"
            model_deployment = os.getenv(f"{prefix}_DEPLOYMENT_NAME", deployment_name)
            token_param = os.getenv(f"{prefix}_TOKEN_PARAM", "max_tokens")
            unsupported_params = (
                os.getenv(f"{prefix}_UNSUPPORTED_PARAMS", "").lower().split(",")
            )
        else:
            model_deployment = deployment_name
            token_param = os.getenv("AZURE_OPENAI_TOKEN_PARAM", "max_tokens")
            unsupported_params = (
                os.getenv("AZURE_OPENAI_UNSUPPORTED_PARAMS", "").lower().split(",")
            )

        # Base parameters for the API call
        params = {
            "model": model_deployment,
            "messages": [
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_prompt},
            ],
        }

        # Add temperature if supported
        if "temperature" not in unsupported_params:
            params["temperature"] = temperature

        # Add the appropriate token parameter based on the model
        if token_param == "max_completion_tokens":
            params["max_completion_tokens"] = max_tokens
        else:
            params["max_tokens"] = max_tokens

        response = client.chat.completions.create(**params)
        return response.choices[0].message.content
    except (ValueError, KeyError, RuntimeError) as e:
        return f"Error: {str(e)}"


def get_available_models():
    """Return a list of available models from environment variables."""
    models = []

    # Add default model if configured
    if os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"):
        models.append(
            {"name": os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"), "type": "default"}
        )

    # Find all model-specific configurations
    for key in os.environ:
        if key.startswith("MODEL_") and key.endswith("_NAME"):
            model_name = os.environ[key]
            model_prefix = key.replace("_NAME", "")
            if os.getenv(f"{model_prefix}_ENDPOINT") and os.getenv(
                f"{model_prefix}_API_KEY"
            ):
                models.append(
                    {
                        "name": model_name,
                        "type": "specific",
                        "id": model_prefix.replace("MODEL_", ""),
                    }
                )

    return models
