"""Run Completion Tab"""

import json
import os
import streamlit as st
from utils.openai_helpers import get_completion, setup_client
from utils.file_helpers import save_completion
from utils.constants import COMPLETIONS_DIR
from utils.document_extraction import extract_text
from utils.document_extraction import is_document_intelligence_available


def render(
    system_messages,
    user_prompts,
    data_files,
    available_models,
    selected_model,
    deployment_name,
    temperature,
    max_tokens,
    save_completion_history=False,
):
    """Render the Run Completion tab
    Args:
        system_messages (dict): Dictionary of system messages.
        user_prompts (dict): Dictionary of user prompts.
        data_files (dict): Dictionary of data files.
        available_models (list): List of available models.
        selected_model (str): Selected model name.
        deployment_name (str): Deployment name for Azure OpenAI.
        temperature (float): Temperature for completion.
        max_tokens (int): Maximum tokens for completion.
        save_completion_history (bool): Flag to save completion history.
    """
    # Initialize session state for storing completion data
    if "completion_data" not in st.session_state:
        st.session_state.completion_data = None
    if "completion_generated" not in st.session_state:
        st.session_state.completion_generated = False

    st.header("Run Completion")

    # DOCUMENT SELECTION SECTION (moved to the top)
    st.subheader("1. Select Documents for Comparison")

    # Updated supported formats to include all Document Intelligence formats
    st.markdown(
        "Supported formats: **PDF**, **JPEG**, **JPG**, **PNG**, **BMP**, **TIFF**, **DOCX**, **XLSX**, **PPTX**, **HTML**, **TXT**, **JSON**"
    )

    # Document Processing Options moved here
    doc_intelligence_available = is_document_intelligence_available()
    use_document_intelligence = st.checkbox(
        "Use Azure Document Intelligence (better quality)",
        value=doc_intelligence_available,  # Default to true if available
        disabled=not doc_intelligence_available,
        help="Uses Azure Document Intelligence for higher quality text extraction. Requires API credentials.",
    )

    if not doc_intelligence_available:
        st.info(
            "Azure Document Intelligence is not available. Set AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT and AZURE_DOCUMENT_INTELLIGENCE_API_KEY environment variables to enable it."
        )

    # Select data files
    col1, col2 = st.columns(2)
    data_file_keys = list(data_files.keys()) if data_files else ["No data files found"]

    with col1:
        data_file1 = st.selectbox(
            "Select Quote 1 Document", data_file_keys, key="data1"
        )
        # Display file content based on file type
        if data_file1 in data_files:
            file_path = data_files[data_file1]
            file_ext = os.path.splitext(file_path)[1].lower()

            st.caption(f"File type: {file_ext[1:].upper()}")

            # For JSON files, show the parsed content
            if file_ext == ".json":
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        quote1_data = json.load(f)
                    st.json(quote1_data, expanded=False)
                except json.JSONDecodeError as e:
                    st.error(f"Error parsing JSON: {str(e)}")
            # For other files, show preview in expander
            else:
                with st.expander("Preview content"):
                    # Pass the use_document_intelligence flag to extract_text for previews
                    content = extract_text(
                        file_path, use_document_intelligence=use_document_intelligence
                    )
                    st.markdown(
                        content[:1000] + ("..." if len(content) > 1000 else ""),
                        unsafe_allow_html=True,
                    )

    with col2:
        # Set default index to 1 (second file) if multiple files exist, otherwise 0
        default_index = (
            min(1, len(data_file_keys) - 1) if len(data_file_keys) > 1 else 0
        )
        data_file2 = st.selectbox(
            "Select Quote 2 Document",
            data_file_keys,
            index=default_index,
            key="data2",
        )
        # Display file content based on file type
        if data_file2 in data_files:
            file_path = data_files[data_file2]
            file_ext = os.path.splitext(file_path)[1].lower()

            st.caption(f"File type: {file_ext[1:].upper()}")

            # For JSON files, show the parsed content
            if file_ext == ".json":
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        quote2_data = json.load(f)
                    st.json(quote2_data, expanded=False)
                except json.JSONDecodeError as e:
                    st.error(f"Error parsing JSON: {str(e)}")
            # For other files, show preview in expander
            else:
                with st.expander("Preview content"):
                    # Pass the use_document_intelligence flag to extract_text for previews
                    content = extract_text(
                        file_path, use_document_intelligence=use_document_intelligence
                    )
                    st.markdown(
                        content[:1000] + ("..." if len(content) > 1000 else ""),
                        unsafe_allow_html=True,
                    )

    # SYSTEM MESSAGE SECTION (collapsed by default)
    st.subheader("2. Configure Prompt")

    with st.expander("System Message", expanded=False):
        # Select system message
        selected_system_message = st.selectbox(
            "Select System Message", list(system_messages.keys())
        )
        system_message_content = system_messages[selected_system_message]
        system_message_editor = st.text_area(
            "Edit System Message", system_message_content, height=200
        )

    # USER PROMPT SECTION (collapsed by default)
    with st.expander("User Prompt Template", expanded=False):
        # Select user prompt
        selected_user_prompt = st.selectbox(
            "Select User Prompt", list(user_prompts.keys())
        )
        user_prompt_template = user_prompts[selected_user_prompt]
        user_prompt_editor = st.text_area(
            "Edit User Prompt Template", user_prompt_template, height=200
        )

    # Load data files using the document extraction functionality
    quote1 = ""
    quote2 = ""
    if data_files and data_file1 in data_files and data_file2 in data_files:
        try:
            quote1 = extract_text(
                data_files[data_file1],
                use_document_intelligence=use_document_intelligence,
            )
            quote2 = extract_text(
                data_files[data_file2],
                use_document_intelligence=use_document_intelligence,
            )
        except Exception as e:
            st.error(f"Error loading data files: {str(e)}")

    # Format user prompt with data
    formatted_user_prompt = user_prompt_editor.format(quote1=quote1, quote2=quote2)

    # Display formatted user prompt
    with st.expander("View Formatted User Prompt", expanded=False):
        st.text_area(
            "Formatted User Prompt",
            formatted_user_prompt,
            height=200,
            disabled=True,
        )

    # Run completion
    st.subheader("3. Generate Comparison")
    # Show save status notification
    if save_completion_history:
        st.info(
            "Completion history saving is enabled. Results will be saved in history."
        )
    else:
        st.warning(
            "Completion history saving is disabled. Results will not be saved automatically."
        )

    run_button_clicked = st.button(
        "Run Completion", type="primary", use_container_width=True
    )

    if run_button_clicked:
        if not selected_model and not deployment_name:
            st.error("Please select a model or provide a deployment name")
        else:
            with st.spinner("Getting completion from Azure OpenAI..."):
                # Get the model ID for specific models
                model_id = None
                for model in available_models:
                    if model["name"] == selected_model and model["type"] == "specific":
                        model_id = model["id"]

                # Setup client with model-specific credentials if available
                client = setup_client(model_id)
                if client:
                    # Get completion using selected model
                    completion = get_completion(
                        client=client,
                        deployment_name=deployment_name if deployment_name else None,
                        system_message=system_message_editor,
                        user_prompt=formatted_user_prompt,
                        temperature=temperature,
                        max_tokens=max_tokens,
                        model_name=model_id,
                    )

                    # Store the completion data in session state
                    st.session_state.completion_data = {
                        "system_message": system_message_editor,
                        "user_prompt": formatted_user_prompt,
                        "completion": completion,
                        "data_file1": data_file1,
                        "data_file2": data_file2,
                        "temperature": temperature,
                        "max_tokens": max_tokens,
                        "model": selected_model,
                    }
                    st.session_state.completion_generated = True

                    # Display completion
                    st.subheader("Completion Result")
                    st.markdown(completion)

                    # Save completion with model information only if enabled
                    if save_completion_history:
                        filename = save_completion(st.session_state.completion_data)
                        st.success(f"Completion saved to {COMPLETIONS_DIR}/{filename}")

    # Show manual save button if completiSSon was generated and auto-save is disabled
    if st.session_state.completion_generated and not save_completion_history:
        if st.button(
            "💾 Save This Completion", type="secondary", key="manual_save_button"
        ):
            filename = save_completion(st.session_state.completion_data)
            st.success(f"Completion manually saved to {COMPLETIONS_DIR}/{filename}")
            # Reset the completion generated flag to avoid double saves
            st.session_state.completion_generated = False
