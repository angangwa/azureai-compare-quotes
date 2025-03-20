"""File handling functions for system messages, user prompts, and completions."""
import os
import json
import glob
from datetime import datetime
import streamlit as st
from utils.constants import (
    SYSTEM_MESSAGES_DIR,
    USER_PROMPTS_DIR,
    DATA_DIR,
    COMPLETIONS_DIR,
    DEFAULT_SYSTEM_MESSAGE,
    DEFAULT_USER_PROMPT,
)


def load_system_messages():
    """Load all saved system messages."""
    system_messages = {"Default": DEFAULT_SYSTEM_MESSAGE}
    for file_path in glob.glob(f"{SYSTEM_MESSAGES_DIR}/*.txt"):
        name = os.path.basename(file_path).replace(".txt", "")
        with open(file_path, "r", encoding="utf-8") as f:
            system_messages[name] = f.read()
    return system_messages


def load_user_prompts():
    """Load all saved user prompts."""
    user_prompts = {"Default": DEFAULT_USER_PROMPT}
    for file_path in glob.glob(f"{USER_PROMPTS_DIR}/*.txt"):
        name = os.path.basename(file_path).replace(".txt", "")
        with open(file_path, "r", encoding="utf-8") as f:
            user_prompts[name] = f.read()
    return user_prompts


def load_data_files():
    """Load all data files from the data directory."""
    data_files = {}
    # Look for files with supported extensions: json, pdf, html, htm, txt, docx
    supported_extensions = ["*.json", "*.pdf", "*.html", "*.htm", "*.txt", "*.docx"]

    for ext in supported_extensions:
        for file_path in glob.glob(f"{DATA_DIR}/{ext}"):
            name = os.path.basename(file_path)
            data_files[name] = file_path
    return data_files


def save_system_message(name, content):
    """Save a system message to file."""
    file_path = f"{SYSTEM_MESSAGES_DIR}/{name}.txt"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    st.success(f"System message '{name}' saved successfully!")


def save_user_prompt(name, content):
    """Save a user prompt to file."""
    file_path = f"{USER_PROMPTS_DIR}/{name}.txt"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    st.success(f"User prompt '{name}' saved successfully!")


def load_completions():
    """Load all saved completions from the completions directory."""
    completions = {}
    os.makedirs(COMPLETIONS_DIR, exist_ok=True)
    for file_path in glob.glob(f"{COMPLETIONS_DIR}/*.json"):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                completion_data = json.load(f)
                file_name = os.path.basename(file_path)
                completions[file_name] = completion_data
        except json.JSONDecodeError as e:
            print(f"Error loading completion {file_path}: {str(e)}")
    return completions


def rename_completion(old_filename, new_name):
    """Rename a completion file while preserving the timestamp."""
    # Extract timestamp if present in the original filename
    timestamp_part = ""
    if "_" in old_filename:
        # Split filename to extract the timestamp portion
        parts = old_filename.split("_", 1)
        if len(parts) > 1 and parts[0] == "completion":
            # Keep the timestamp part
            timestamp_part = f"_{parts[1]}"

    # Ensure the new name ends with timestamp and .json
    if not timestamp_part:  # If no timestamp found, keep original behavior
        if not new_name.endswith(".json"):
            new_name = f"{new_name}.json"
    else:
        # Remove .json from new_name if present
        if new_name.endswith(".json"):
            new_name = new_name[:-5]
        # Ensure the timestamp is preserved
        if "_" in new_name:  # If new name already has a timestamp format, use as is
            new_name = f"{new_name}.json"
        else:
            new_name = f"{new_name}{timestamp_part}"

    old_path = f"{COMPLETIONS_DIR}/{old_filename}"
    new_path = f"{COMPLETIONS_DIR}/{new_name}"

    if os.path.exists(new_path):
        return False, f"A file with name '{new_name}' already exists."

    try:
        os.rename(old_path, new_path)
        return True, f"Renamed completion to '{new_name}'"
    except OSError as e:
        return False, f"Error renaming file: {str(e)}"


def delete_completion(filename):
    """Delete a completion file."""
    file_path = f"{COMPLETIONS_DIR}/{filename}"

    try:
        os.remove(file_path)
        return True, f"Deleted completion '{filename}'"
    except OSError as e:
        return False, f"Error deleting file: {str(e)}"


def save_completion(completion_data):
    """Save a completion to file with timestamp."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    completion_data["timestamp"] = timestamp

    os.makedirs(COMPLETIONS_DIR, exist_ok=True)
    filename = f"completion_{timestamp}.json"
    file_path = f"{COMPLETIONS_DIR}/{filename}"

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(completion_data, f, indent=4)

    return filename
