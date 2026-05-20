# core/scheduler.py
import json, threading, time, datetime, os
from commands.speak import speak
from commands.reminders import REMINDER_FILE

class ReminderScheduler:
    def __init__(self, poll_seconds: int = 30):
        self.poll_seconds = poll_seconds
        self._stop = threading.Event()
        self._thread = None
        self._last_fired = set()  # (task,time,date) to avoid repeats

    def start(self):
        if self._thread and self._thread.is_alive():
            return
        self._stop.clear()
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def stop(self):
        self._stop.set()

    def _loop(self):
        while not self._stop.is_set():
            try:
                now = datetime.datetime.now()
                due = self._load_due(now)
                for label in due:
                    if label in self._last_fired:
                        continue
                    # speak and mark fired
                    speak(f"Reminder: {label[0]}")
                    self._last_fired.add(label)
            except Exception as e:
                print("[scheduler] error:", e)
            finally:
                time.sleep(self.poll_seconds)

    def _load_due(self, now):
        if not os.path.exists(REMINDER_FILE):
            return []
        try:
            with open(REMINDER_FILE, "r") as f:
                items = json.load(f)
        except Exception:
            return []
        # Expect each item like {"task": "...", "time": "7:30 PM", "date": "2025-08-23"} or without date = today
        due = []
        today = now.date().isoformat()
        for r in items:
            t_str = r.get("time", "")
            d_str = r.get("date", today) or today
            try:
                # parse "7:30 PM" naive today
                hhmm = datetime.datetime.strptime(t_str.strip(), "%I:%M %p").time()
                if d_str != today:
                    continue
                target = datetime.datetime.combine(now.date(), hhmm)
                if 0 <= (now - target).total_seconds() <= self.poll_seconds:
                    due.append((r.get("task",""), t_str, d_str))
            except Exception:
                continue
        return due
