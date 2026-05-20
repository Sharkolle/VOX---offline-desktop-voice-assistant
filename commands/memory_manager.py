# commands/memory_manager.py

# This module handles all memory-related commands for VOX.
# Features:
# - Switching user profiles
# - Remembering key-value pairs (e.g., "my name is...")
# - Recalling stored information (e.g., "what's my name?")

import string
from core.memory import (
    store_memory,
    recall_memory,
    load_memory,
    save_memory,
    set_active_user,
    get_active_user,
    get_user_file,
)

def handle_memory_command(command: str) -> dict:
    """
    Handles commands related to user memory and profile management.

    Supported:
    - "Switch to user [username]" → Switch active user profile
    - "Remember [key] is [value]" → Store data
    - "My name is [value]" → Alternative way to store name
    - "What’s my [key]?" → Recall stored data

    Returns:
        dict: {'text': str, 'speak': str} → spoken and displayed response
    """

    # Auto-set a default active user if none is set
    if get_active_user() is None:
        set_active_user("default")

    command = command.lower()

    # 1️⃣ SWITCH USER: Example → "switch to user Ahmad"
    if "switch to user" in command:
        try:
            username = command.split("switch to user")[1].strip()
            set_active_user(username)
            return {
                "text": f"Switched to user profile '{username}'.",
                "speak": f"Switched to user profile '{username}'."
            }
        except Exception as e:
            print("[ERROR]", e)
            return {
                "text": "I couldn’t switch profiles. Please try again.",
                "speak": "I couldn’t switch profiles. Please try again."
            }

    # 2️⃣ STORE MEMORY: Example → "remember my favorite color is blue"
    elif "remember" in command and " is " in command:
        try:
            parts = command.split("remember")[1].strip()
            key, value = parts.split(" is ", 1)
            key = key.strip().replace("my ", "")
            value = value.strip()
            store_memory(key, value)
            return {
                "text": f"Got it. I’ll remember your {key} is {value}.",
                "speak": f"I’ll remember your {key} is {value}."
            }
        except Exception:
            return {
                "text": "Sorry, I didn’t catch what I should remember.",
                "speak": "I didn’t catch what I should remember."
            }

    # 3️⃣ Alternative STORE → Example: "my name is Ahmad"
    elif "my name is" in command:
        try:
            value = command.split("my name is", 1)[1].strip()
            key = "name"

            # Store in the correct active user file
            active_user = get_active_user()
            store_memory(key, value, get_user_file(active_user))

            response_text = f"Okay, your name is {value}."
            return {"text": response_text, "speak": response_text}
        except Exception:
            return {
                "text": "I didn’t catch your name.",
                "speak": "I didn’t catch your name."
            }

    # 4️⃣ RECALL MEMORY: Example → "what's my name?" / "what is my favorite color?"
    elif "what's my" in command or "what is my" in command:
        try:
            key = command.replace("what's my", "").replace("what is my", "").strip()
            key = key.strip(string.punctuation).strip()
            value = recall_memory(key)

            if value:
                return {
                    "text": f"Your {key} is {value}.",
                    "speak": f"Your {key} is {value}."
                }
            else:
                return {
                    "text": f"I don’t know your {key} yet.",
                    "speak": f"I don’t know your {key} yet."
                }
        except Exception:
            return {
                "text": "I didn’t understand what you want me to recall.",
                "speak": "I didn’t understand what you want me to recall."
            }

    # If command doesn’t match anything here → return None for fallback handling
    return None







