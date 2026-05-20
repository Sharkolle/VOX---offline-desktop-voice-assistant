def handle_help_command() -> dict:
    """
        Generate a help message outlining the available commands VOX can handle.

        Returns:
            dict: Contains both 'text' for terminal output and 'speak' for voice output.
        """
    help_text = """
Here's what I can help you with:

🔸 Time & Date
- "What time is it?"
- "What's today's date?"

🔸 System Control
- "Open calculator" or "Open browser"
- "Shutdown system" / "Restart system" / "Lock system"
- "Take a screenshot"
- "Empty recycle bin"

🔸 Reminders
- "Remind me to [task] at [time]"
- "What are my reminders?"
- "Delete reminder for [task] at [time]"

🔸 User Memory
- "Remember my name is [name]"
- "What's my name?"

🔸 Fun Stuff
- "Tell me a joke"
- "Motivate me"
- "Say something cool"

🔸 Web Search
- "Search [your query]"

🔸 Media
- "Increase the volume" / "Decrease the volume"
- "Mute volume" / "Play or Pause media"

🔸 Modes & Configuration
- "Switch to offline mode" / "Switch to online mode"
- "What mode are you in?"

🔸 Conversation Memory
- "What did I say?" or "Repeat what you said"

🔸 Daily Briefing
- "Good morning" → Full report with date, reminders, motivation

🔸 Help
- "Help" → Displays this guide

"""

    return {
        "text": help_text,
        "speak": "Here's a summary of the commands you can use. Please check your terminal for the full list."
    }
