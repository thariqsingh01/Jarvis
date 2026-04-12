import os
import datetime

# ==========================
# LOGGING HELPER
# ==========================
def save_note(note_content: str, filename="jarvis_notes.txt"):
    """
    Saves a note with a timestamp to a file.
    Returns path of saved file.
    """
    path = os.path.join(os.getcwd(), filename)
    try:
        with open(path, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.datetime.now()}] {note_content}\n")
        return path
    except Exception as e:
        return None


# ==========================
# FILE PATH HELPERS
# ==========================
def get_desktop_path(filename=""):
    """
    Returns the full path to the current user's Desktop
    Optionally appends a filename
    """
    desktop = os.path.join(os.environ["USERPROFILE"], "Desktop")
    return os.path.join(desktop, filename) if filename else desktop


# ==========================
# SIMPLE UTILITY EXAMPLE
# ==========================
def format_response(text: str):
    """
    Utility to standardize backend responses if needed
    """
    return {"response": text}