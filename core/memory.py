# core/memory.py

# This module handles VOX's memory system.
# - Stores key-value data for *each user* (e.g., name, preferences).
# - Remembers last command and last response.
# - Data is persistent (saved to disk as JSON).

import os
import json

# Tracks the *current* active user during runtime
current_active_user = None

# Location for the file that saves the currently active user between sessions
CURRENT_PROFILE_FILE = "data/current_user.txt"

def get_user_file(user: str) -> str:
    """
    Returns the file path for a given user's memory file.

    Args:
        user (str): Username.

    Returns:
        str: Path to the JSON file for that user.
    """
    return f"data/{user}_memory.json"


def set_active_user(name: str) -> str:
    """
    Sets the active user and ensures their memory file exists.

    Args:
        name (str): Username to activate.

    Returns:
        str: Path to the active user's memory file.
    """
    global current_active_user
    current_active_user = name

    with open(CURRENT_PROFILE_FILE, 'w') as f:
        f.write(name.lower().strip())

    user_file = get_user_file(name)
    os.makedirs(os.path.dirname(user_file), exist_ok=True)

    if not os.path.exists(user_file):
        with open(user_file, "w") as file:
            json.dump({"name": name}, file, indent=4)
    else:
        memory = load_memory(user_file)
        if memory.get("name") != name:
            memory["name"] = name
            save_memory(memory, user_file)

    return user_file


def load_memory(user_file: str = None) -> dict:
    """
    Loads memory data for the active user (or specified user).

    Args:
        user_file (str, optional): Specific file to load. Defaults to active user.

    Returns:
        dict: Memory data.
    """
    if user_file is None:
        if current_active_user is None:
            raise ValueError("No active user is set. Call set_active_user(name) first.")
        user_file = get_user_file(current_active_user)

    if not os.path.exists(user_file):
        return {}

    with open(user_file, "r") as file:
        return json.load(file)


def save_memory(memory: dict, user_file: str = None):
    """
    Saves the provided memory dictionary to disk.

    Args:
        memory (dict): Data to save.
        user_file (str, optional): Specific file to save. Defaults to active user.
    """
    if user_file is None:
        if current_active_user is None:
            raise ValueError("No active user is set. Call set_active_user(name) first.")
        user_file = get_user_file(current_active_user)

    with open(user_file, "w") as file:
        json.dump(memory, file, indent=4)


def store_memory(key: str, value: str, user_file: str = None):
    """
    Stores a key-value pair in memory for the active (or provided) user.

    Args:
        key (str): Key to store.
        value (str): Value to associate with the key.
        user_file (str, optional): Memory file to use.
    """
    if user_file is None:
        user_file = get_user_file(get_active_user())

    memory = load_memory(user_file)
    memory[key] = value
    save_memory(memory, user_file)


def recall_memory(key: str, user_file: str = None):
    """
    Retrieves the value for a given key from memory.

    Args:
        key (str): Key to retrieve.
        user_file (str, optional): Memory file to use.

    Returns:
        str or None: Value associated with key, or None if not found.
    """
    if user_file is None:
        user_file = get_user_file(get_active_user())

    memory = load_memory(user_file)
    return memory.get(key)


def set_last_interaction(user_command: str, response: str):
    """
    Stores the latest interaction (user command + VOX response),
    and maintains only the last 5 in memory.
    """
    memory = load_memory()
    interaction = {"command": user_command, "response": response}

    # Load existing interaction history (if any)
    last_interactions = memory.get("last_interactions", [])

    # Add new one to the front
    last_interactions.insert(0, interaction)

    # Keep only the last 5
    memory["last_interactions"] = last_interactions[:5]

    save_memory(memory)



def get_last_user_command() -> str:
    """
    Retrieves the last command spoken by the user.

    Returns:
        str: The last command, or a fallback message.
    """
    memory = load_memory()
    return memory.get("last_user_command", "You haven’t said anything yet.")


def get_last_response() -> str:
    """
    Retrieves the last response VOX gave to the user.

    Returns:
        str: The last response, or a fallback message.
    """
    memory = load_memory()
    return memory.get("last_response", "I haven’t said anything yet.")


def get_active_user() -> str:
    """
    Returns the current active user (from runtime or stored file).

    Returns:
        str: Active username or 'default'.
    """
    global current_active_user
    if current_active_user:
        return current_active_user

    if os.path.exists(CURRENT_PROFILE_FILE):
        with open(CURRENT_PROFILE_FILE, "r") as f:
            user = f.read().strip()
            current_active_user = user
            return user

    return "default"

def get_last_interactions() -> list:
    """
    Retrieves the last 5 interactions (if available).

    Returns:
        list of dicts: [{command, response}, ...]
    """
    memory = load_memory()
    return memory.get("last_interactions", [])



