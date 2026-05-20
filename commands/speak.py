# commands/speak.py

# This module defines the speak() function for VOX.
# It uses the offline TTS engine 'pyttsx3' to convert text to spoken audio.
# Works completely offline → no internet or external APIs required.

# core/speak.py

import os
import time
import tempfile
import pyttsx3
import pygame
from gtts import gTTS
from core.config import get_mode
# Initialize pyttsx3 engine (offline voice)
offline_engine = pyttsx3.init()
offline_engine.setProperty('rate', 180)  # Optional: Adjust speaking rate

def use_offline_voice(text):
    """
    Speak using offline pyttsx3 voice.
    """
    offline_engine.say(text)
    offline_engine.runAndWait()

def use_online_voice(text):
    """
    Speak using Google Text-to-Speech (requires internet) and play with pygame.
    """
    try:
        # Generate TTS MP3
        tts = gTTS(text)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            temp_audio = fp.name
            tts.save(temp_audio)

        # Play using pygame
        pygame.mixer.init()
        pygame.mixer.music.load(temp_audio)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

        pygame.mixer.quit()
        os.remove(temp_audio)

    except Exception as e:
        print(f"[!] Online voice error: {e}")
        print("[!] Falling back to offline voice...")
        use_offline_voice(text)

def speak(text, mode="offline"):
    """
    Universal speak function. Selects between offline and online modes.
    mode: 'offline' (default) or 'online'
    """
    if get_mode() == "online":
        use_online_voice(text)
    else:
        use_offline_voice(text)



