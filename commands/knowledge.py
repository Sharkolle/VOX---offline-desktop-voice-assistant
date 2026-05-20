# knowledge.py

# 📚 This module handles simple knowledge questions using Wikipedia (online for now).
# If the command matches a topic, VOX will fetch a short summary.
# ⚠️ Can be upgraded later to use offline models or local GPTs.

import wikipedia
from commands.speak import speak

def handle_knowledge_query(command: str) -> dict:
    """
    Handles questions by searching Wikipedia for a summary.
    """
    try:
        # Use the command as the search query
        summary = wikipedia.summary(command, sentences=2)
        return {"text": summary, "speak": summary}

    except wikipedia.exceptions.DisambiguationError as e:
        response = f"That topic is too broad. Try being more specific."

        return {"text": response, "speak": response}

    except wikipedia.exceptions.PageError:
        response = f"I couldn’t find any information about {command}."

        return {"text": response, "speak": response}

    except Exception:
        response = "Something went wrong trying to get that information."

        return {"text": response, "speak": response}

