# commands/config_commands.py

# ⚙️ This module handles VOX's configuration commands.
# Allows switching between online/offline modes by voice.

from core.config import get_mode, set_mode


def handle_config_command(command: str) -> dict:
    command = command.lower()

    if "offline mode" in command or "switch to offline" in command:
        set_mode("offline")
        response = "Switched to offline mode."  # Defined for this branch
    elif "online mode" in command or "switch to online" in command:
        set_mode("online")
        response = "Switched to online mode."  # Defined for this branch
    elif "what mode" in command:
        current_mode = get_mode()
        response = f"The assistant is currently in {current_mode} mode."
    else:
        response = "I’m not sure how to handle that config request."  # Fallback

    return {"text": response,
            "speak": response}
