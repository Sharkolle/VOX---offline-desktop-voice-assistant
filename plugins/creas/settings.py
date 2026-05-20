# core/settings.py

import json
import os

SETTINGS_PATH = "settings.json"
DEFAULT_SETTINGS = {
    "theme": "light",
    "font_size": "medium"
}

def load_settings():
    if not os.path.exists(SETTINGS_PATH):
        save_settings(DEFAULT_SETTINGS)
    with open(SETTINGS_PATH, "r") as f:
        return json.load(f)

def save_settings(settings):
    with open(SETTINGS_PATH, "w") as f:
        json.dump(settings, f, indent=4)
