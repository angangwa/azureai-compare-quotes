"""Functionality to render the Completion History tab in the Streamlit app."""
import streamlit as st
from utils.file_helpers import rename_completion, delete_completion, load_completions
from utils.formatting import format_timestamp, get_friendly_completion_name


def render(_):
    """Render the Completion History tab"""
    st.header("Completion History")

    # Add a refresh button
    if st.button("🔄 Refresh Completion History"):
        st.rerun()

    # Always reload completions to get the latest data
    fresh_completions = load_completions()

    if not fresh_completions:
        st.info("No saved completions found.")
        return

    st.info(f"Found {len(fresh_completions)} saved completions.")

    # Display completions
    for filename, data in sorted(
        fresh_completions.items(),
        key=lambda x: x[1].get("timestamp", ""),
        reverse=True,
    ):
        # Get friendly display name for the expander
        friendly_name = get_friendly_completion_name(filename)

        with st.expander(f"{friendly_name}"):
            # Display completion details with formatted timestamp
            timestamp = data.get("timestamp", "N/A")
            formatted_time = format_timestamp(timestamp)
            st.markdown(f"**Timestamp:** {formatted_time}")
            st.markdown(f"**Model:** {data.get('model', 'N/A')}")
            st.markdown(f"**Quote 1:** {data.get('data_file1', 'N/A')}")
            st.markdown(f"**Quote 2:** {data.get('data_file2', 'N/A')}")

            # Use tabs instead of nested expanders
            content_tabs = st.tabs(
                ["Completion Result", "System Message", "User Prompt"]
            )

            with content_tabs[0]:
                st.markdown(data.get("completion", "No completion data available"))

            with content_tabs[1]:
                # Add unique key for system message text area
                st.text_area(
                    "System Message",
                    data.get("system_message", ""),
                    height=100,
                    disabled=True,
                    key=f"system_msg_{filename}",
                )

            with content_tabs[2]:
                # Add unique key for user prompt text area
                st.text_area(
                    "User Prompt",
                    data.get("user_prompt", ""),
                    height=100,
                    disabled=True,
                    key=f"user_prompt_{filename}",
                )

            # Rename and delete functionality
            st.markdown("---")
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                new_name = st.text_input(
                    f"New name for {filename}", key=f"new_name_{filename}"
                )
            with col2:
                if st.button("Rename", key=f"rename_{filename}"):
                    if new_name:
                        success, message = rename_completion(filename, new_name)
                        if success:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)
                    else:
                        st.error("Please provide a new name")
            with col3:
                if st.button("🗑️ Delete", key=f"delete_{filename}"):
                    success, message = delete_completion(filename)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
