# task_router.py

"""
Task Router for VOX
--------------------
This module routes incoming user commands to the appropriate handlers.
It acts as the central brain that decides *what* function to call for any given spoken command.
"""
from commands.config_settings import handle_settings_command
from commands.memory_manager import handle_memory_command
from commands.search_web import search_google
from commands.tell_time import tell_time
from commands.tell_date import tell_date
from commands.fun_skills import handle_fun_command
from commands.open_app import open_application
from commands.reminders import handle_reminder_command, list_all_reminders, delete_reminder, extract_task_time
from commands.system_control import shutdown_system, confirm_action, restart_system, lock_system, logout_system, sleep_system, toggle_wifi, brightness_adjust, \
    run_system_diagnosis
from commands.daily_briefing import daily_briefing
from commands.system_control import take_screenshot, empty_recycle_bin, play_pause_media, volume_up, volume_down, mute_volume
from core.memory import set_last_interaction
from commands.conversation_memory import handle_conversation_memory
from commands.config_commands import handle_config_command
from commands.help import handle_help_command
from commands.knowledge import handle_knowledge_query
from plugins.creas.storage import save_note
from plugins.creas.recognizer import recognize_offline
from commands.todo import add_item, list_items, remove_item, clear_list
from commands.wraper import wrap

def fallback_response(command: str) -> dict:
    """
    Returns a default fallback response when VOX doesn’t understand the command.
        """
    response = (
        f"Sorry, I’m not sure how to handle \"{command}\" yet. "
        "You can say 'help' to hear what I can do."
    )
    return {"text": response, "speak": response}
def handle_command(command_text: str) -> dict:
    """
    Routes the user's voice command to the correct handler/module.

    Args:
        command_text (str): The recognized speech converted to text.

    Returns:
        dict: Response with 'text' and 'speak' keys for displaying and speaking.
    """
    if not command_text:
        return {
            "text": "No command received.",
            "speak": "Sorry, I didn't hear anything."
        }

    #Check memory commands first
    response = handle_memory_command(command_text)
    if response:
        return response

    #Check reminder commands
    reminder_res = handle_reminder_command(command_text)
    if reminder_res:
        return reminder_res

    #Fun responses (jokes, quotes, etc.)
    fun_response = handle_fun_command(command_text)
    if fun_response:
        return fun_response

    #Convert to lowercase for easier matching
    command_text = command_text.lower()

    #Application & System commands
    if "open" in command_text:
        return open_application(command_text)

    elif "search" in command_text:
        query = command_text.replace("search", "").strip()
        return search_google(query)

    elif "shutdown" in command_text or "shut down" in command_text:
        return shutdown_system() if confirm_action("shutdown") else {"text": "Shutdown canceled.",
                                                                     "speak": "Shutdown request canceled."}

    elif "restart" in command_text:
        return restart_system() if confirm_action("restart") else {"text": "Restart canceled.",
                                                                   "speak": "Restart request canceled."}

    elif "log out" in command_text or "log out system" in command_text:
        return logout_system() if confirm_action("log out") else {"text": "Logout canceled.",
                                                                  "speak": "Logout request canceled."}

    elif any(word in command_text for word in
             ["settings", "change voice", "speak faster", "speak slower", "set volume", "reset settings",
              "what are my settings"]):
        return handle_settings_command(command_text)

    elif "screenshot" in command_text or "screen shot" in command_text:
        return take_screenshot()

    elif "empty recycle bin" in command_text:
        return empty_recycle_bin()

    elif "sleep" in command_text or "sleep mode" in command_text:
        return sleep_system()

    elif "lock" in command_text or "lock system" in command_text:
        return lock_system()

    elif "increase the volume" in command_text or "volume up" in command_text or "increase volume" in command_text:
        return volume_up()

    elif "decrease the volume" in command_text or "volume down" in command_text or "decrease volume" in command_text:
        return volume_down()

    elif "mute" in command_text:
        return mute_volume()

    elif "play" in command_text or "pause" in command_text:
        return play_pause_media()

    elif "offline mode" in command_text or "online mode" in command_text or "what mode" in command_text or "switch to offline" in command_text or "switch to online" in command_text:
        return handle_config_command(command_text)

    #Information & Conversation
    if any(p in command_text for p in ["add to my list", "add to the list", "add on my list", "todo add"]):
        text = command_text
        for p in ["add to my list", "add to the list", "add on my list", "todo add"]:
            text = text.replace(p, "").strip(":, ").strip()
        return wrap(command_text, add_item(text))
    if "what's on my list" in command_text or "show my list" in command_text or "list my todo" in command_text:
        return wrap(command_text, list_items())
    if any(p in command_text for p in ["remove from my list", "delete from, my list", "todo remove"]):
        text = command_text
        for p in ["remove from my list", "delete from, my list", "todo remove"]:
            text = text.replace(p, "").strip(":, ").strip()
        return wrap(command_text, remove_item(text))
    if "clear my list" in command_text or "empty my list" in command_text or "clear todo" in command_text:
        return wrap(command_text, clear_list())
    elif "time" in command_text:
        return tell_time()

    elif "date" in command_text:
        return tell_date()

    elif "good morning" in command_text or "briefing" in command_text or "good evening" in command_text:
        return daily_briefing()

    elif any(keyword in command_text for keyword in ["what did i say", "repeat", "what did you say", "conversation", "history"]):
        return handle_conversation_memory(command_text)

    elif any(keyword in command_text for keyword in ["delete reminder", "remove reminder"]):
        task, time_str = extract_task_time(command_text)
        if task and time_str:
            return delete_reminder(task, time_str)
        else:
            return {
                "text": "Please specify: 'Delete reminder for [task] at [time]'",
                "speak": "Sorry, I need to know which reminder to delete. Say something like: Delete my meeting reminder at 3 PM"
            }

    elif "who is" in command_text or "what is" in command_text:
        return handle_knowledge_query(command_text)

    elif "what are my reminders" in command_text or "list my reminders" in command_text:
        return list_all_reminders()

    elif "wifi" in command_text or "wi-fi" in command_text:
        return toggle_wifi()

    elif "brightness" in command_text:
        if "up"in command_text or "increase" in command_text:
            return brightness_adjust()
        elif "down" in command_text or "decrease" in command_text or "adjust" in command_text:
            return brightness_adjust(level="down")

    elif "run system diagnosis" in command_text or "system diagnosis" in command_text:
        return run_system_diagnosis()

    # --- NOTES / NOTE MODE ROUTES ---

    text_lc = command_text.lower().strip()
    if ("note mode" in text_lc) or ("open notes" in text_lc):
        return {"text": "Opening Note mode...", "speak": "Opening note mode."}

    if text_lc.startswith("take a note"):
        raw = command_text.split("take a note", 1)[1]
        note_text = raw.lstrip(":, ").strip()

        if note_text:
            name = save_note(note_text)
            return {"text": f"Noted: {note_text}  (saved as {name})", "speak": "Noted."}

        transcript = recognize_offline(duration=5)
        if transcript:
            name = save_note(transcript)
            return {"text": f"Noted: {transcript}  (saved as {name})", "speak": "Noted."}
        return {"text": "I didn’t hear anything to note.", "speak": "I didn’t hear anything to note."}



    elif "help" in command_text or "what can you do" in command_text:
        return handle_help_command()


    #If vox don’t know what the command means → fallback
    set_last_interaction(command_text, fallback_response(command_text)["speak"])
    return fallback_response(command_text)


