# core/storage.py

import os
import datetime

NOTES_DIR = "notes"
os.makedirs(NOTES_DIR, exist_ok=True)

def get_new_note_id():
    existing_notes = [
        f for f in os.listdir(NOTES_DIR)
        if f.endswith(".txt") and f.startswith("note_")
    ]
    ids = []
    for f in existing_notes:
        try:
            number = int(f.split("_")[1].split(".")[0])
            ids.append(number)
        except ValueError:
            continue

    next_id = max(ids, default=0) + 1
    return next_id

def save_note(transcript: str, audio_path: str = None):
    try:
        note_id = get_new_note_id()
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        note_name = f"note_{note_id:03d}"
        text_path = os.path.join(NOTES_DIR, f"{note_name}.txt")

        with open(text_path, "w", encoding="utf-8") as f:
            f.write(f"[{timestamp}]\n")
            f.write(transcript.strip() + "\n")

        print(f"✅ Note saved as: {note_name}")
        return note_name

    except Exception as e:
        print(f"❌ Failed to save note: {e}")
        return None
