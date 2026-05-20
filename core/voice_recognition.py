# core/voice_recognition.py

# This module handles voice recognition for VOX.
# It supports two modes:
# → ONLINE → Uses Google's Speech Recognition API.
# → OFFLINE → Uses Whisper AI (faster-models) locally.
#
# Mode is controlled by → core/config.py → ('online' or 'offline')

import speech_recognition as sr
import sounddevice as sd
import numpy as np
from faster_whisper import WhisperModel
from core.config import get_mode

# Initialize the Whisper models for offline recognition (only if needed)
try:
    if get_mode() == "offline":
        model = WhisperModel("base.en", device="cpu", compute_type="int8")
except Exception as e:
    print("[ERROR] Whisper base.en failed to load:", e)
    model = None



def listen_and_recognize():
    '''
    Listens to microphone input and converts speech to text.
    Uses online or offline recognition depending on VOX's mode.

    Returns:
        str or None: The recognized text, or None if recognition fails.
    '''
    mode = get_mode()

    if mode == "online":
        return _recognize_online()
    elif mode == "offline":
        return _recognize_offline()
    else:
        print(f"Invalid mode: {mode}")
        return None


def _recognize_online() -> str:
    """
    Uses the online Google Speech Recognition API to transcribe speech.

    Returns:
        str or None: Recognized speech, or None if recognition fails.
    """
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Adjusting for ambient noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source, duration=1)

        print("Listening for your command...")
        try:
            audio = recognizer.listen(source, timeout=5)
            print("Voice captured. Processing...")
        except sr.WaitTimeoutError:
            print("No speech detected. Please try again.")
            return None

    # Convert speech to text using Google_API
    try:
        command_text = recognizer.recognize_google(audio)
        print(f"Recognized command: {command_text}")
        return command_text
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand what you said.")
    except sr.RequestError:
        print("Sorry, there's a problem reaching the speech service.")

    return None


def _recognize_offline() -> str:
    """
    Uses the offline Whisper AI models to transcribe speech.

    Returns:
        str or None: Recognized speech, or None if recognition fails.
    """
    print("\n=== Listening (speak now) ===")

    fs = 16000  # Sampling rate (Hz)
    duration = 5  # Recording duration (seconds)

    try:
        # Record from microphone
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float32')
        sd.wait()

        # Transcribe with Whisper_model
        segments, info = model.transcribe(np.squeeze(recording), beam_size=5)
        transcript = " ".join(segment.text for segment in segments).strip()

        if transcript:
            print(f"Recognized: {transcript}")
            return transcript
        else:
            print("No speech detected.")
            return None

    except Exception as e:
        print(f"Offline recognition error: {e}")
        return None
            

# --- Unified helpers so other modules don't create models ---

def recognize_for_seconds(seconds: int = 5) -> str:
    """
    Record from the default mic for a fixed duration and return a transcript
    using the same offline/online pipeline VOX already uses.
    """

    samplerate = 16000
    frames = int(samplerate * seconds)
    with sd.InputStream(samplerate=samplerate, channels=1, dtype="float32") as stream:
        chunks = []
        remaining = frames
        block = int(samplerate * 0.25)  # 250ms blocks
        while remaining > 0:
            n = min(block, remaining)
            data, _ = stream.read(n)
            chunks.append(data.copy())
            remaining -= n
    audio = np.squeeze(np.concatenate(chunks, axis=0))  # (N,)

    # Reuse current pipeline (offline/online depending on config)
    # If you already have a function that takes raw audio, call it here.
    try:
        return transcribe_audio_buffer(audio, samplerate)  # see next helper
    except NameError:

        return listen_and_recognize()


def transcribe_audio_buffer(audio_float32, samplerate: int = 16000) -> str:
    """
    Given a mono float32 numpy array, return a transcript using the same
    offline model VOX uses (faster-whisper). If online mode is set, you can
    choose to route to the online recognizer instead.
    """

    # If you want to honor online mode, you can branch here.
    # mode = get_mode()
    # if mode == "online": <send audio to your online recognizer if implemented>

    # Offline (faster-whisper) path — reuse the global/model your module already manages.
    try:
        from faster_whisper import WhisperModel
    except Exception:
        return ""

    audio = np.asarray(audio_float32, dtype="float32").squeeze()
    if audio.size == 0:
        return ""

    model = getattr(globals(), "WHISPER_MODEL", None)
    if model is None:
        try:
            import os
            from pathlib import Path
            models_dir = Path(__file__).resolve().parents[1] / "models"
            for cand in (models_dir / "base.en", models_dir / "tiny.en"):
                if cand.exists():
                    model = WhisperModel(str(cand), device="cpu", compute_type="int8")
                    break
            if model is None:
                model = WhisperModel("base.en", device="cpu", compute_type="int8")
            globals()["WHISPER_MODEL"] = model
        except Exception:
            model = WhisperModel("tiny.en", device="cpu", compute_type="int8")
            globals()["WHISPER_MODEL"] = model

    segments, _ = model.transcribe(
        audio, beam_size=2, vad_filter=True, language=None
    )
    return " ".join(s.text for s in segments).strip()
