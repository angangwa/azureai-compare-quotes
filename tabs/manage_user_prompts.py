"""Manage User Prompts Tab"""
import streamlit as st
from utils.file_helpers import save_user_prompt


def render(user_prompts):
    """Render the Manage User Prompts tab"""
    st.header("Manage User Prompts")

    # Add new user prompt
    st.subheader("Add New User Prompt")
    new_prompt_name = st.text_input("User Prompt Name")
    new_prompt_content = st.text_area("User Prompt Content", height=200)
    st.info("Use {quote1} and {quote2} placeholders in your prompt template")
    if st.button("Save User Prompt"):
        if new_prompt_name:
            save_user_prompt(new_prompt_name, new_prompt_content)
            st.rerun()
        else:
            st.error("Please provide a name for the user prompt")

    # View existing user prompts
    st.subheader("Existing User Prompts")
    for name, content in user_prompts.items():
        with st.expander(f"User Prompt: {name}"):
            st.text_area(f"Content for {name}", content, height=200, disabled=True)
