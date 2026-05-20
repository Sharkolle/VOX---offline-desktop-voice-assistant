# plugins/note_mode/gui.py
import os
import tkinter as tk
from tkinter import messagebox
import sounddevice as sd
import soundfile as sf

# Reuse VOX STT helpers (single engine for the whole app)
from core.voice_recognition import recognize_for_seconds, transcribe_audio_buffer

# Plugin-local imports (no hard-coded package name)
from plugins.creas.settings import load_settings, save_settings
from plugins.creas.live_recorder import LiveRecorder
from plugins.creas.storage import save_note, NOTES_DIR


class SilentNoteGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SilentNote")
        self.root.geometry("600x500")
        self.root.resizable(False, False)

        self.recorder = LiveRecorder()
        self.is_recording = False

        self.settings = load_settings()
        self.font_sizes = {"small": 10, "medium": 12, "large": 14}

        self._bg = None
        self._fg = None
        self._btn_bg = None

        self.build_interface()
        self.apply_theme()
        self.load_notes()  # show existing notes on open

    # ---------- THEME ----------
    def apply_theme(self):
        theme = self.settings.get("theme", "light")
        font_size = self.font_sizes.get(self.settings.get("font_size", "medium"), 12)

        bg = "#f0f0f0" if theme == "light" else "#121212"
        fg = "#000000" if theme == "light" else "#ffffff"
        btn_bg = "#e0e0e0" if theme == "light" else "#1e1e1e"

        self._bg, self._fg, self._btn_bg = bg, fg, btn_bg

        self.root.configure(bg=bg)

        # Apply to title, status label, and buttons
        self.title_label.configure(bg=bg, fg=fg, font=("Helvetica", font_size + 4, "bold"))
        self.status_label.configure(bg=bg, fg=fg, font=("Helvetica", font_size))

        self.start_button.configure(bg=btn_bg, fg=fg, font=("Helvetica", font_size))
        self.stop_button.configure(bg=btn_bg, fg=fg, font=("Helvetica", font_size))
        self.settings_button.configure(bg=btn_bg, fg=fg, font=("Helvetica", font_size))

        # Notes list container background
        self.notes_view.configure(bg=bg)

    # ---------- AUDIO PLAYBACK ----------
    def play_audio(self, audio_path):
        try:
            data, samplerate = sf.read(audio_path, dtype='float32')
            sd.play(data, samplerate)
            self.status_label.config(text=f"Playing: {os.path.basename(audio_path)}", fg="blue")
        except Exception as e:
            messagebox.showerror("Playback Error", f"Could not play audio: {e}")

    # ---------- SETTINGS ----------
    def open_settings_window(self):
        win = tk.Toplevel(self.root)
        win.title("Settings")
        win.geometry("300x200")
        win.resizable(False, False)

        bg, fg = self._bg, self._fg
        win.configure(bg=bg)

        # Theme toggle
        tk.Label(win, text="Theme:", bg=bg, fg=fg).pack(pady=5)
        theme_var = tk.StringVar(value=self.settings.get("theme", "light"))
        tk.OptionMenu(win, theme_var, "light", "dark").pack()

        # Font size
        tk.Label(win, text="Font Size:", bg=bg, fg=fg).pack(pady=5)
        font_var = tk.StringVar(value=self.settings.get("font_size", "medium"))
        tk.OptionMenu(win, font_var, "small", "medium", "large").pack()

        # Save Button
        def save_changes():
            self.settings["theme"] = theme_var.get()
            self.settings["font_size"] = font_var.get()
            save_settings(self.settings)
            self.apply_theme()
            win.destroy()

        tk.Button(win, text="Apply", command=save_changes, bg="#007bff", fg="white").pack(pady=10)

    # ---------- UI ----------
    def build_interface(self):
        self.title_label = tk.Label(self.root, text="📝 SilentNote", font=("Helvetica", 18, "bold"))
        self.title_label.pack(pady=10)

        self.status_label = tk.Label(self.root, text="Status: Idle", font=("Helvetica", 12))
        self.status_label.pack()

        # Start button
        self.start_button = tk.Button(
            self.root, text="🎙 Start Recording", font=("Helvetica", 14),
            command=self.start_recording, bg="#28a745", fg="white", width=20
        )
        self.start_button.pack(pady=5)

        # Stop button
        self.stop_button = tk.Button(
            self.root, text="🛑 Stop & Save", font=("Helvetica", 14),
            command=self.stop_recording, bg="#ffc107", fg="black", width=20, state=tk.DISABLED
        )
        self.stop_button.pack(pady=5)

        # Settings Button
        self.settings_button = tk.Button(self.root, text="⚙ Settings", command=self.open_settings_window)
        self.settings_button.pack(pady=(10, 5))

        # Notes viewer (scrollable frame inside a canvas)
        canvas = tk.Canvas(self.root, width=580, height=250, highlightthickness=0)
        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        self.notes_view = tk.Frame(canvas)

        self.notes_view.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=self.notes_view, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True, padx=10)
        scrollbar.pack(side="right", fill="y")

        # Close only this window (don’t quit VOX)
        tk.Button(
            self.root, text="❌ Close", font=("Helvetica", 12),
            command=self.root.destroy, bg="#dc3545", fg="white"
        ).pack(pady=5)

    # ---------- NOTES ----------
    def load_notes(self):
        for widget in self.notes_view.winfo_children():
            widget.destroy()

        notes = [f for f in os.listdir(NOTES_DIR) if f.endswith(".txt")]
        if not notes:
            lbl = tk.Label(self.notes_view, text="No saved notes yet.", anchor="w", justify="left",
                           bg=self._bg, fg=self._fg)
            lbl.pack(fill="x", padx=10, pady=5)
            return

        for note_file in sorted(notes):
            base_name = note_file[:-4]  # strip .txt
            txt_path = os.path.join(NOTES_DIR, note_file)
            wav_path = os.path.join(NOTES_DIR, f"{base_name}.wav")

            # Read text
            with open(txt_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Note container
            frame = tk.Frame(self.notes_view, bg=self._bg, bd=1, relief="solid")
            frame.pack(fill="x", padx=10, pady=5)

            # Text
            note_label = tk.Label(
                frame, text=f"📝 {note_file}\n{content}", anchor="w", justify="left",
                bg=self._bg, fg=self._fg, font=("Helvetica", 12)
            )
            note_label.pack(side="left", padx=10, pady=5, fill="both", expand=True)

            # ▶️ Play button
            if os.path.exists(wav_path):
                tk.Button(frame, text="▶️ Play", command=lambda p=wav_path: self.play_audio(p)).pack(side="right", padx=10)

    # ---------- RECORD ----------
    def start_recording(self):
        try:
            note_id = f"note_{len(os.listdir(NOTES_DIR)) // 2 + 1:03d}"
            self.audio_path = os.path.join(NOTES_DIR, f"{note_id}.wav")

            self.recorder.start(self.audio_path)
            self.status_label.config(text="Status: Recording…", fg="green")
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start recording: {e}")

    def stop_recording(self):
        try:
            self.recorder.stop()
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.status_label.config(text="Status: Idle", fg=self._fg)

            # Read the saved audio and transcribe with VOX pipeline
            audio_data, sr = sf.read(self.audio_path, dtype="float32")
            transcript = transcribe_audio_buffer(audio_data, samplerate=sr)

            if transcript:
                name = save_note(transcript, self.audio_path)
                messagebox.showinfo("Note Saved", f"Note saved as {name}")
                self.load_notes()
            else:
                messagebox.showinfo("No Speech", "No speech detected.")
        except Exception as e:
            messagebox.showerror("Error", f"Recording failed: {e}")


def open_silentnote_window(parent):
    """Open SilentNote as a child window inside VOX."""
    win = tk.Toplevel(parent)
    SilentNoteGUI(win)
    return win
