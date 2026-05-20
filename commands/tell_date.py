# commands/tell_date.py

# 📅 This module handles requests for the current date.
# Example output: "Today is Tuesday, June 4, 2025."

from datetime import datetime

def tell_date() -> dict:
    """
    Returns the current date in a human-readable format.

    Returns:
        dict: {'text': str, 'speak': str} → for display and spoken response.
    """
    today = datetime.now()
    formatted_date = today.strftime("%A, %B %d, %Y")

    return {
        "text": f"Today's date is {formatted_date}.",
        "speak": f"Today is {formatted_date}."
    }

