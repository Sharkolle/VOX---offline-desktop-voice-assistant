# commands/reminders.py

# ⏰ This module allows VOX to save, list, and check reminders.
# Example usage:
# → "Remind me to train at 8 PM"
# → Reminder is stored in reminders.json for future notification.

import json
import os
import re
from datetime import datetime
from core.memory import load_memory

REMINDER_FILE = "data/reminders.json"


def normalize_time_format(text: str) -> str:
    """
    Normalizes spoken or written time strings for processing.

    Example:
        '7.30 pm' → '7:30 PM'
        '7PM' → '7 PM'

    Args:
        text (str): The raw time input from user.

    Returns:
        str: Normalized time string.
    """
    # Convert '7.30' → '7:30'
    text = re.sub(r"(\d+)\.(\d+)", r"\1:\2", text)
    text = text.replace("pm", "PM").replace("am", "AM")

    # Insert space before AM/PM → '7PM' → '7 PM'
    text = re.sub(r"(\d)(AM|PM)", r"\1 \2", text)

    return text.strip()


def add_reminder(task: str, time_str: str) -> dict:
    """
    Adds a reminder to the JSON file.

    Args:
        task (str): The reminder task text (e.g., "train").
        time_str (str): The time for the reminder (e.g., "8 PM").

    Returns:
        dict: Confirmation text and speech.
    """
    clean_time_str = normalize_time_format(time_str)
    os.makedirs(os.path.dirname(REMINDER_FILE), exist_ok=True)
    clean_time_str = clean_time_str.replace(".", "").upper()

    # Validate and format time
    try:
        time_obj = datetime.strptime(clean_time_str, "%I:%M %p")
        formatted_time = time_obj.strftime("%I:%M %p")
    except ValueError:
        try:
            time_obj = datetime.strptime(clean_time_str, "%I %p")  # Example: 8 PM
            formatted_time = time_obj.strftime("%I:%M %p")
        except ValueError:
            return {
                "text": "Invalid time format. Please say something like '5:30 PM'.",
                "speak": "I couldn’t understand the time. Try something like 5:30 PM."
            }

    # Load existing reminders
    if os.path.exists(REMINDER_FILE):
        with open(REMINDER_FILE, "r") as file:
            reminders = json.load(file)
    else:
        reminders = []

    # Add the new reminder
    reminders.append({
        "task": task,
        "time": formatted_time,
        "reminded": False
    })

    with open(REMINDER_FILE, "w") as file:
        json.dump(reminders, file, indent=4)

    return {
        "text": f"Reminder set: {task} at {formatted_time}.",
        "speak": f"I'll remind you to {task} at {formatted_time}."
    }


def list_all_reminders() -> dict:
    """
    Lists all saved reminders for the current user.

    Returns:
        dict: Reminders combined as a text response.
    """
    if not os.path.exists(REMINDER_FILE):
        response = "You have no saved reminders."
        return {"text": response, "speak": response}

    with open(REMINDER_FILE, "r") as file:
        reminders = json.load(file)

    if reminders:
        formatted = [f"{r['task']} at {r['time']}" for r in reminders]
        response = "Here are your reminders: " + "; ".join(formatted)
    else:
        response = "You have no saved reminders."

    return {"text": response, "speak": response}



def handle_reminder_command(command: str) -> dict:
    """
    Parses and processes spoken reminder commands.

    Args:
        command (str): Example → "remind me to pray at 5:30 pm"

    Returns:
        dict: Success or failure message.
    """
    command = command.lower()

    if "remind me to" in command and " at " in command:
        try:
            parts = command.split("remind me to")[1].strip()
            task, time_part = parts.rsplit(" at ", 1)
            task = task.strip()
            time_part = time_part.strip().upper()
            return add_reminder(task, time_part)
        except:
            return {
                "text": "I couldn’t understand your reminder format.",
                "speak": "I didn’t understand what to remind you about."
            }


def check_reminders():
    """
    Checks if any saved reminders match the current time.

    Returns:
        list or None: List of due reminders, or None if none are due.
    """
    if not os.path.exists(REMINDER_FILE):
        return None

    with open(REMINDER_FILE, "r") as file:
        reminders = json.load(file)

    now_time = datetime.now().strftime("%I:%M %p")
    updated = False
    due_reminders = []

    for reminder in reminders:
        if reminder["time"] == now_time and not reminder.get("reminded", False):
            due_reminders.append(reminder)
            reminder["reminded"] = True
            updated = True

    if updated:
        with open(REMINDER_FILE, "w") as file:
            json.dump(reminders, file, indent=4)

    return due_reminders if due_reminders else None

def normalize_time_str(time_str: str) -> str:
    """
    Normalize time string for consistent comparison.
    E.g., "6:16 p.m." -> "6:16 PM" without leading zeros.

    Args:
        time_str (str): Time string to normalize.

    Returns:
        str: Normalized time string or cleaned fallback if parsing fails.
    """
    clean_time = re.sub(r'[^0-9:apmAPM\s]', '', time_str).strip().upper()
    try:
        time_obj = datetime.strptime(clean_time, "%I:%M %p")
        return time_obj.strftime("%I:%M %p").lstrip('0')
    except ValueError:
        try:
            time_obj = datetime.strptime(clean_time, "%I %p")
            return time_obj.strftime("%I:%M %p").lstrip('0')
        except ValueError:
            # fallback: return cleaned string anyway (may fail to match)
            return clean_time


def delete_reminder(task: str, time_str: str) -> dict:
    """
    Deletes a specific reminder matching the provided task and time.

    Args:
        task (str): The task description to delete.
        time_str (str): The time string (e.g., "7:30 AM").

    Returns:
        dict: {'text': str, 'speak': str} → feedback for display and speech.
    """
    if not os.path.exists(REMINDER_FILE):
        return {
            "text": "You don’t have any reminders saved.",
            "speak": "You don’t have any reminders saved."
        }

    with open(REMINDER_FILE, "r") as file:
        reminders = json.load(file)

    original_len = len(reminders)

    # Normalize the time string given in the command
    clean_time = normalize_time_str(time_str)

    # Filter out the reminder matching both task and normalized time
    reminders = [
        r for r in reminders
        if not (
            r['task'].lower() == task.lower()
            and normalize_time_str(r['time']) == clean_time
        )
    ]

    if len(reminders) == original_len:
        return {
            "text": f"No reminder found for '{task}' at {clean_time}.",
            "speak": f"I couldn't find a reminder for {task} at {clean_time}."
        }

    # Save the updated reminders list
    with open(REMINDER_FILE, "w") as file:
        json.dump(reminders, file, indent=4)

    return {
        "text": f"Deleted reminder: '{task}' at {clean_time}.",
        "speak": f"Deleted your reminder for {task}."
    }


def extract_task_time(command_text: str):
    """
    Extracts 'task' and 'time' from deletion commands like:
    → 'delete reminder to [TASK] at [TIME]'

    Returns:
        tuple: (task, time_str) or (None, None) if no match
    """
    # Regex pattern supports flexible phrasing → handles:
    # "delete the reminder to [task] at [time]"
    # "delete reminder for [task] at [time]"
    pattern = r"delete (?:the )?reminder (?:to|for|about) (.+?) (?:at|for) (.+)"
    match = re.search(pattern, command_text, re.IGNORECASE)
    if match:
        task = match.group(1).strip()
        time_str = match.group(2).strip()
        return task, time_str
    return None, None
