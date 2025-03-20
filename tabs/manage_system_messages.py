"""Manage System Messages Tab"""

import streamlit as st
from utils.file_helpers import save_system_message


def render(system_messages):
    """Render the Manage System Messages tab"""
    st.header("Manage System Messages")

    # Add new system message
    st.subheader("Add New System Message")
    new_system_name = st.text_input("System Message Name")
    new_system_content = st.text_area("System Message Content", height=200)
    if st.button("Save System Message"):
        if new_system_name:
            save_system_message(new_system_name, new_system_content)
            st.rerun()
        else:
            st.error("Please provide a name for the system message")

    # View existing system messages
    st.subheader("Existing System Messages")
    for name, content in system_messages.items():
        with st.expander(f"System Message: {name}"):
            st.text_area(f"Content for {name}", content, height=200, disabled=True)
