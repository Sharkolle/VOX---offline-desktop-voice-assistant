# commands/conversation_memory.py

#  This module allows VOX to recall recent conversation.
# It supports repeating the user's last command or VOX's last response.

# commands/conversation_memory.py

"""
Conversation Memory
--------------------
This module allows VOX to recall the last thing you said,
what it responded, or even a history of past commands.
"""

from core.memory import get_last_user_command, get_last_response, get_last_interactions


def handle_conversation_memory(command: str) -> dict:
    """
    Handles memory-related commands like:
    → "What did I say?"
    → "What did you say?"
    → "Repeat"
    → "What was our last conversation?"

    Args:
        command (str): The user’s spoken command.

    Returns:
        dict: Response to speak and display.
    """
    command = command.lower()

    if "what did i say" in command:
        last = get_last_user_command()
        return {
            "text": f"You said: {last}",
            "speak": f"You said: {last}"
        }

    elif "what did you say" in command or "what was your reply" in command:
        last = get_last_response()
        return {
            "text": f"I said: {last}",
            "speak": f"I said: {last}"
        }

    elif "repeat" in command:
        return {
            "text": get_last_response(),
            "speak": get_last_response()
        }

    elif "conversation" in command or "history" in command:
        interactions = get_last_interactions()

        if not interactions:
            return {
                "text": "I don’t remember anything yet.",
                "speak": "I don’t remember anything yet."
            }

        combined = []
        for i, pair in enumerate(interactions, 1):
            combined.append(f"{i}. You said: {pair['command']} → I replied: {pair['response']}")

        response_text = "\n".join(combined)
        return {
            "text": response_text,
            "speak": f"I remember the last {len(interactions)} things we talked about."
        }

    return None

