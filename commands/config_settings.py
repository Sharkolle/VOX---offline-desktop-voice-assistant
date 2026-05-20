# commands/config_settings.py

import pyttsx3
from core.memory import load_memory, save_memory, get_active_user
import re

DEFAULT_SETTINGS = {
    "voice": "default",     # You can map this to index 0 or 1
    "rate": 150,
    "volume": 0.9
}

engine = pyttsx3.init()

def apply_settings(settings):
    """Apply current voice settings to the speech engine."""
    voices = engine.getProperty("voices")

    # Set voice
    if settings.get("voice") == "female" and len(voices) > 1:
        engine.setProperty("voice", voices[1].id)
    else:
        engine.setProperty("voice", voices[0].id)

    # Set rate & volume
    engine.setProperty("rate", settings.get("rate", 150))
    engine.setProperty("volume", settings.get("volume", 0.9))


def handle_settings_command(command: str) -> dict:
    user_file = f"data/{get_active_user()}_memory.json"
    memory = load_memory(user_file)

    # Load or initialize settings
    settings = {
        "voice": memory.get("voice", "default"),
        "rate": memory.get("rate", 150),
        "volume": memory.get("volume", 0.9)
    }

    # Lowercase for parsing
    cmd = command.lower()

    # --- Voice Switching ---
    if "change voice" in cmd:
        if settings["voice"] == "female":
            settings["voice"] = "default"
            response = "Switched to default voice."
        else:
            settings["voice"] = "female"
            response = "Switched to female voice."

    # --- Speed Control ---
    elif "speak faster" in cmd:
        settings["rate"] += 25
        response = f"Speaking faster. New rate is {settings['rate']}."

    elif "speak slower" in cmd:
        settings["rate"] = max(75, settings["rate"] - 25)
        response = f"Speaking slower. New rate is {settings['rate']}."

    # --- Volume Adjustment ---
    elif "set volume to" in cmd:
        match = re.search(r"volume to (\d+)", cmd)
        if match:
            vol = int(match.group(1)) / 100
            settings["volume"] = min(max(vol, 0.0), 1.0)
            response = f"Volume set to {int(settings['volume'] * 100)} percent."
        else:
            response = "Please specify the volume percentage. For example, say: set volume to 80 percent."

    # --- View Settings ---
    elif "what are my settings" in cmd:
        response = (
            f"Current settings: Voice = {settings['voice']}, "
            f"Rate = {settings['rate']}, Volume = {int(settings['volume'] * 100)}%"
        )

    # --- Reset ---
    elif "reset settings" in cmd:
        settings = DEFAULT_SETTINGS.copy()
        response = "Settings reset to default."

    else:
        return {
            "text": "I didn't understand your settings request.",
            "speak": "Please say something like change voice or set volume to 70 percent."
        }

    # Save settings to memory
    memory.update(settings)
    save_memory(memory, user_file)
    apply_settings(settings)

    return {"text": response, "speak": response}
