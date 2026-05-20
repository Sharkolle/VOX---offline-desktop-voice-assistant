# commands/daily_briefing.py

# 🌅 This module generates a daily briefing combining:
# - Today's date
# - Any reminders set for the day
# - A motivational quote or fun fact

from datetime import datetime
from commands.reminders import check_reminders
from commands.fun_skills import handle_fun_command

def daily_briefing() -> dict:
    """
    Generates a daily briefing message for the user, including:
    1. The current date
    2. Today's reminders (if any)
    3. A motivational quote

    Returns:
        dict: {'text': str, 'speak': str} → for screen display and speech output
    """

    # 1️⃣ Get current date and format it nicely
    now = datetime.now()
    date_text = now.strftime("Today is %A, %B %d, %Y.")

    # 2️⃣ Retrieve any reminders for today
    reminders = check_reminders()
    if reminders:
        reminder_text = "Here are your reminders: " + ", ".join(reminders)
    else:
        reminder_text = "You have no reminders today."

    # 3️⃣ Get a motivational quote from fun_skills
    motivation = handle_fun_command("motivate me")["speak"]

    # 4️⃣ Combine everything into one complete briefing
    full_text = f"{date_text}\n{reminder_text}\nToday's Motivation: {motivation}"

    # 5️⃣ Return the combined text for both display and speaking
    return {
        "text": full_text,
        "speak": full_text
    }
