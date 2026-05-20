# commands/tell_time.py

# ⏰ This module handles requests for the current time.
# Example output → "The current time is 08:45 PM."
import os
from datetime import datetime

def tell_time() -> dict:
    """
    Returns the current system time in a readable format.

    Returns:
        dict: {'text': str, 'speak': str} → for display and spoken output.
    """
    current_time = datetime.now().strftime("%I:%M %p")

    return {
        "text": f"The current time is {current_time}.",
        "speak": f"The current time is {current_time}."
    }
