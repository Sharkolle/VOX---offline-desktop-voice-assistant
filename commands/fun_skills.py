# commands/fun_skills.py

# This module handles VOX's fun and personality-based commands.
# VOX can:
# - Tell programming & tech jokes
# - Provide motivational quotes
# - Say something cool or clever
# - Respond to "who created you?"

import random

def handle_fun_command(command: str) -> dict:
    """
    Handles fun-related commands, such as telling a joke, giving motivation, or saying something cool.

    Supported commands:
    - "tell me a joke"
    - "motivate me" / "give me motivation"
    - "say something cool"
    - "who created you"

    Returns:
        dict: {'text': str, 'speak': str} → output for display and speech
    """
    command = command.lower()

    # Jokes list (mostly programming, tech, and AI-themed)
    jokes = [
        "Why do Python developers prefer snakes? Because they hate *indentation errors*.",
        "Why did the JavaScript developer quit? He didn’t get *promises*.",
        "Why do programmers hate nature? Too many *bugs*.",
        "What’s a programmer’s favorite hangout? *Foo Bar*.",
        "Why did the SQL query break up with the NoSQL database? It needed *commitment*.",
        # (... additional jokes ...)
    ]

    # Motivational quotes → coding, persistence, mindset
    motivation = [
        "Your code today is better than your no-code yesterday.",
        "Debugging is like being a detective—every error is a clue.",
        "The best way to predict the future is to *code* it.",
        "Failure is just the *first iteration* of success.",
        "The only wrong code is the one you never write.",
        # (... additional quotes ...)
    ]

    # Cool lines → witty, philosophical, AI-flavored
    cool_lines = [
        "I don’t predict the future—I *train* it.",
        "I don’t sleep—I *process*.",
        "My code is *self-improving*—just like me.",
        "Reality is just a *simulation*—debug wisely.",
        "Wisdom is *lossless compression* of experience.",
        # (... additional lines ...)
    ]

    # Creator response
    w_c_y = "I have been created by Ahmad, a Nigerian software developer, and he's still working on improving me."

    # 🗣️ Command matching → pick random item from the appropriate list
    if "joke" in command:
        line = random.choice(jokes)
        return {"text": line, "speak": line}

    elif "motivate" in command or "motivation" in command:
        line = random.choice(motivation)
        return {"text": line, "speak": line}

    elif "something cool" in command or "say something cool" in command:
        line = random.choice(cool_lines)
        return {"text": line, "speak": line}

    elif "who created you" in command:
        line = w_c_y
        return {"text": line, "speak": line}

    # ⚠️ Return None if command is unrecognized by this module
    return None

