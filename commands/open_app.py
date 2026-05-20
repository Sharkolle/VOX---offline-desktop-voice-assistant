# commands/open_app.py
"""This module will:

Receive a command like “open browser” or “open notepad”

Detect which app the user wants

Use os.system() or subprocess to open it

Return a dict with:

"text" for terminal display

"speak" for voice feedback"""

import subprocess
import sys
import os
import platform


def open_application(command: str) -> dict:
    command = command.lower()

    def open_browser():
        if sys.platform == "win32":
            subprocess.run(["start", "https://google.com"], shell=True, check=False)
        elif sys.platform == "darwin":
            subprocess.run(["open", "https://google.com"], check=False)
        else:  # Linux
            subprocess.run(["xdg-open", "https://google.com"], check=False)

    def open_notepad():
        if sys.platform == "win32":
            subprocess.run(["notepad"], shell=True, check=False)
        elif sys.platform == "darwin":
            subprocess.run(["open", "-a", "TextEdit"], check=False)
        else:  # Linux
            subprocess.run(["xdg-open", "--tempfile"], check=False)

    def open_file_explorer():
        if sys.platform == "win32":
            subprocess.run(["explorer"], shell=True, check=False)
        elif sys.platform == "darwin":
            subprocess.run(["open", "."], check=False)
        else:  # Linux
            subprocess.run(["xdg-open", "."], check=False)

    def open_calculator():
        if sys.platform == "win32":
            subprocess.run(["calc"], shell=True, check=False)
        elif sys.platform == "darwin":
            subprocess.run(["open", "-a", "Calculator"], check=False)
        else:  # Linux
            subprocess.run(["gnome-calculator"] if sys.platform == "linux" else ["kcalc"], check=False)

    def open_recycle_bin():
        system = platform.system()

        if system == "Windows":
            os.system("explorer.exe shell:RecycleBinFolder")
        elif system == "Linux":
            # Linux typically uses trash:/// URI for opening trash
            os.system("xdg-open trash:///")
        elif system == "Darwin":
            # macOS opens Trash in Finder
            os.system("open ~/.Trash")
        else:
            return {
                "text": "Recycle bin access not supported on this OS.",
                "speak": "Sorry, I can't open the recycle bin on this system yet."
            }

    def open_settings():
        system = platform.system()
        if system == "Windows":
            subprocess.run(["start", "ms-settings:"], shell=True, check=False)
        elif system == "Darwin":
            subprocess.run(["open", "-a", "System Preferences"], check=False)
        else:  # Linux - comprehensive approach for different desktop environments
            # Try to detect desktop environment
            desktop = os.environ.get("XDG_CURRENT_DESKTOP", "").lower()

            if "gnome" in desktop or "unity" in desktop:
                subprocess.run(["gnome-control-center"], check=False)
            elif "kde" in desktop:
                subprocess.run(["systemsettings5"], check=False)
            elif "xfce" in desktop:
                subprocess.run(["xfce4-settings-manager"], check=False)
            elif "mate" in desktop:
                subprocess.run(["mate-control-center"], check=False)
            elif "cinnamon" in desktop:
                subprocess.run(["cinnamon-settings"], check=False)
            elif "lxde" in desktop:
                subprocess.run(["lxappearance"], check=False)
            elif "pantheon" in desktop:
                subprocess.run(["switchboard"], check=False)
            elif "budgie" in desktop:
                subprocess.run(["budgie-desktop-settings"], check=False)
            else:
                # Fallback methods
                try:
                    # Try universal settings command
                    subprocess.run(["systemsettings"], check=False)
                except:
                    # Final fallback to xdg-open
                    subprocess.run(["xdg-open", "settings:"], check=False)

    keywords = ['browser', 'chrome', 'firefox', 'internet']
    if any(k in command for k in keywords):
        open_browser()
        return {
            "text": "opening browser....",
            "speak": "here is your browser"
        }

    elif "notepad" in command:
        open_notepad()
        return {
            "text": "Opening text editor...",
            "speak": "Opening text editor for you."
        }

    elif "explorer" in command or "files" in command:
        open_file_explorer()
        return {
            "text": "Opening file manager...",
            "speak": "Here's your file manager."
        }

    elif "calculator" in command or "calc" in command:
        open_calculator()
        return {
            "text": "Opening calculator...",
            "speak": "Calculator coming up."
        }

    elif "recycle bin" in command:
        open_recycle_bin()
        return {
            "text": "Opening recycle bin...",
            "speak": "Recycle bin opened."
        }

    elif "settings" in command or "control panel" in command or "system preferences" in command:
        open_settings()
        return {
            "text": "Opening system settings...",
            "speak": "System settings are now open."
        }

    else:
        return {
            "text": "I don’t recognize that application.",
            "speak": "Sorry, I don't know how to open that yet."
        }
