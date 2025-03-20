"""Streamlit application for comparing quotes using Azure OpenAI."""

import os
import streamlit as st
from dotenv import load_dotenv

# Import from utility modules
from utils.constants import (
    SYSTEM_MESSAGES_DIR,
    USER_PROMPTS_DIR,
    DATA_DIR,
    COMPLETIONS_DIR,
    ABOUT_THIS_APP,
)
from utils.openai_helpers import setup_client, get_available_models
from utils.file_helpers import (
    load_system_messages,
    load_user_prompts,
    load_data_files,
    load_completions,
)

# Import tab modules
from tabs.run_completion import render as render_run_completion
from tabs.manage_system_messages import render as render_manage_system_messages
from tabs.manage_user_prompts import render as render_manage_user_prompts
from tabs.completion_history import render as render_completion_history

# Load environment variables
load_dotenv()

# Set page configuration
st.set_page_config(page_title="Comparing quotes", page_icon="🤖", layout="wide")

# Ensure directories exist
for directory in [SYSTEM_MESSAGES_DIR, USER_PROMPTS_DIR, DATA_DIR, COMPLETIONS_DIR]:
    os.makedirs(directory, exist_ok=True)


# Main app
def main():
    """Main function to run the Streamlit app."""
    # App title and description
    st.title("Comparing Quotes using Azure OpenAI")

    # Sidebar for API settings
    st.sidebar.header("About This App")

    st.sidebar.markdown(ABOUT_THIS_APP)

    st.sidebar.header("API Settings")

    # Setup OpenAI client
    setup_client()

    # Get available models
    available_models = get_available_models()
    model_names = [model["name"] for model in available_models]

    # Allow user to select from available models
    selected_model = st.sidebar.selectbox(
        "Select Model",
        model_names,
        index=0 if model_names else None,
    )

    # For backward compatibility
    deployment_name = st.sidebar.text_input(
        "Custom Deployment Name (Optional)",
        value="" if selected_model else os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", ""),
        help="Use this only if you want to override the model's deployment name",
    )

    temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.7, 0.1)
    max_tokens = st.sidebar.number_input("Max Tokens", 1, 4000, 1000, 100)

    # Add option to save completion history
    save_completion_history = st.sidebar.checkbox(
        "Save completion history",
        value=False,
        help="Enable to save the completion results in history",
    )

    # Load available system messages, user prompts, and data files
    system_messages = load_system_messages()
    user_prompts = load_user_prompts()
    data_files = load_data_files()
    completions = load_completions()

    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "Run Completion",
            "Manage System Messages",
            "Manage User Prompts",
            "Completion History",
        ]
    )

    # Render each tab using the imported modules
    with tab1:
        render_run_completion(
            system_messages,
            user_prompts,
            data_files,
            available_models,
            selected_model,
            deployment_name,
            temperature,
            max_tokens,
            save_completion_history,
        )

    with tab2:
        render_manage_system_messages(system_messages)

    with tab3:
        render_manage_user_prompts(user_prompts)

    with tab4:
        render_completion_history(completions)


if __name__ == "__main__":
    main()
