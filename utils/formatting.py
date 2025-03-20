"""Utility functions for formatting strings and timestamps."""

from datetime import datetime


def format_timestamp(timestamp_str):
    """Format a timestamp string like '20240520_153045' to a more readable format."""
    try:
        # Parse the timestamp string to datetime
        dt = datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S")
        # Format it in a more user-friendly way
        return dt.strftime("%B %d, %Y at %H:%M:%S")
    except ValueError:
        # Return the original if parsing fails
        return timestamp_str


def get_friendly_completion_name(filename):
    """Format completion filename to be more user-friendly for display."""
    # Remove .json extension
    if filename.endswith(".json"):
        basename = filename[:-5]
    else:
        basename = filename

    # Extract timestamp if present in the filename
    timestamp_part = None
    name_part = basename

    if "_" in basename:
        # Try to extract timestamp
        parts = basename.rsplit("_", 5)  # YYYYMMDD_HHMMSS has 5 underscores
        if len(parts) >= 2:
            # Check if the last part looks like a timestamp (numbers only)
            potential_timestamp = "_".join(parts[-2:]) if len(parts) > 2 else parts[-1]
            if potential_timestamp.isdigit() or (
                potential_timestamp.count("_") == 1
                and all(p.isdigit() for p in potential_timestamp.split("_"))
            ):
                timestamp_part = potential_timestamp
                name_part = basename[
                    : -(len(timestamp_part) + 1)
                ]  # +1 for the underscore

    # Format the display name
    if name_part == "completion" or name_part == "":
        # Default unnamed completion
        display_name = "Unnamed"
    else:
        display_name = name_part

    # Add formatted timestamp if available
    if timestamp_part:
        try:
            # Format timestamp in a user-friendly way
            dt = datetime.strptime(timestamp_part, "%Y%m%d_%H%M%S")
            friendly_time = dt.strftime("%B %d, %Y at %H:%M:%S")
            return f"{display_name} ({friendly_time})"
        except ValueError:
            pass

    # If timestamp formatting fails, return just the name
    return display_name
