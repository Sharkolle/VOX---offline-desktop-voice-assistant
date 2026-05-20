# core/config.py

# ⚙️ This module handles VOX's configuration settings.
# Currently, → Controls ONLINE or OFFLINE operation mode.
# Configuration is stored in → data/config.json

import json
import os

CONFIG_FILE = "data/config.json"

# Default configuration if config file does not exist yet.
DEFAULT_CONFIG = {
    "mode": "offline"  # Default to offline for privacy/security
}

def load_config() -> dict:
    """
    Loads configuration from the JSON file.

    Returns:
        dict: The configuration settings.
    """
    if not os.path.exists(CONFIG_FILE):
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG

    with open(CONFIG_FILE, "r") as f:
        return json.load(f)


def save_config(config: dict):
    """
    Saves the provided configuration dictionary to the JSON file.

    Args:
        config (dict): The configuration settings to save.
    """
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)


def get_mode() -> str:
    """
    Returns the current mode ('online' or 'offline').

    Returns:
        str: 'online' or 'offline'
    """
    return load_config().get("mode", "online")


def set_mode(mode: str):
    """
    Updates the configuration with a new mode.

    Args:
        mode (str): New mode ('online' or 'offline')
    """
    config = load_config()
    config["mode"] = mode.lower()
    save_config(config)

