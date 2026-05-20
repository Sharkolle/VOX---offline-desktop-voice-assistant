# main_terminal.py
"""
Entry Point for VOX Voice Assistant
-----------------------------------
This is the main driver of the entire VOX assistant.
It listens for wake words, processes user commands, and routes tasks to appropriate modules.
"""
import threading

from core.voice_recognition import listen_and_recognize
from task_router import handle_command
from core.wake_word import wait_for_wake_word
from commands.reminders import check_reminders
from core.memory import get_active_user
from commands.speak import speak
import time
import pyfiglet
import platform
from core.config import get_mode
def print_banner():
    ascii_banner = pyfiglet.figlet_format("VOX", font="slant")
    print("\033[92m" + ascii_banner + "\033[0m")  # Green text

    subtext = "Offline Voice Assistant  •  OmniGuard Technologies"
    print("\033[90m" + subtext + "\033[0m")  # Dim gray text
    print("-" * 50)

def greet_user(username):
    greeting = f"Welcome back, {username}. I am ready to assist you."
    print(f"\n🟢 {greeting}")
    speak(greeting)

def show_system_info():
    print("\n=== VOX SYSTEM CONFIGURATION ===")
    print(f"👤 Username     : {get_active_user()}")
    print(f"🗣️ Voice Mode   : {get_mode()}")
    print(f"🎯 Wake Word    : {get_mode()}")
    print(f"💻 OS           : {platform.system()} {platform.release()}")
    print("================================\n")
    time.sleep(1)

def main():
    print_banner()
    show_system_info()
    greet_user(get_active_user())
    speak("Launching core assistant loop...")
    print("🔄 Starting assistant... [Insert assistant loop here]")

if __name__ == "__main__":
    main()



def main():
    """
    Starts the VOX assistant loop.
    Continuously listens for the wake word, processes user commands, and handles reminders.
    """
    speak("VOX system ready. Say 'Hey VOX' when you need me.")
    wake_stop = threading.Event()
    while True:
        # Check if any reminders are due and announce them
        due = check_reminders()
        if due:
            for reminder in due:
                speak(f"Reminder: {reminder['task']} now.")

        # Wait for wake word ("Hey VOX")
        triggered = wait_for_wake_word(wake_stop)

        if not triggered:
            speak("Exiting...")
            break

        # Listen for spoken command
        command = listen_and_recognize()

        if command is None:
            continue

        # Handle shutdown command by user
        if any(word in command.lower() for word in ["exit", "quit", "stop"]):
            speak("Shutting down. Goodbye.")
            break

        # Route command to appropriate handler and get response
        response = handle_command(command)

        # Print text feedback to console
        print(response["text"])

        #  Speak the response
        speak(response["speak"])


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        speak("Shutting down. Goodbye.")
        print("Exiting program.")
