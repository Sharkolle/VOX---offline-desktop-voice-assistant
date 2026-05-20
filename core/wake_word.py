# core/wake_word.py

"""
Wake Word Detection for VOX (stoppable + robust)
Listens for variations of "hey vox" using faster-whisper (tiny.en by default).
"""

import time
import difflib
from typing import Optional, Callable, Iterable

import numpy as np
import sounddevice as sd

try:
    from faster_whisper import WhisperModel
except Exception:  # avoid crashing if model isn't installed
    WhisperModel = None

# Acceptable variations
WAKE_WORDS: Iterable[str] = (
    "hey vox", "hi vox",
    "hey box", "hi box",
    "hey fox", "hi fox",
    "hey, vox", "hey folks", "hey books", "hey vaux", "hey vocks"
)

# Model singleton (tiny for low CPU)
_MODEL = None


def _ensure_model():
    global _MODEL
    if _MODEL is not None:
        return _MODEL
    if WhisperModel is None:
        return None
    try:
        # tiny.en is fast; switch to "tiny" or "base" if you want multilingual
        _MODEL = WhisperModel("tiny.en", device="cpu", compute_type="int8")
    except Exception as e:
        print("[wake] Failed to load Whisper model:", e)
        _MODEL = None
    return _MODEL


def _heard_wake(text: str, threshold: float = 0.75) -> bool:
    """
    Returns True if 'text' likely contains the wake phrase.
    Uses both fuzzy ratio and substring containment.
    """
    t = (text or "").lower().strip()
    if not t:
        return False
    # direct containment first (fast path)
    if any(p in t for p in WAKE_WORDS):
        return True
    # fuzzy score against best candidate
    best = max(WAKE_WORDS, key=lambda p: difflib.SequenceMatcher(None, t, p).ratio())
    score = difflib.SequenceMatcher(None, t, best).ratio()
    # debug:  print(f"[wake] heard='{t}' best='{best}' score={score:.2f}")
    return score >= threshold


def wait_for_wake_word(
    stop_event,
    *,
    on_detect: Optional[Callable[[str], None]] = None,
    sample_rate: int = 16000,
    window_sec: float = 1.2,
    overlap_windows: int = 2,
    cooldown_sec: float = 2.0,
    threshold: float = 0.75,
) -> Optional[str]:
    """
    Blocking loop that returns the detected phrase (or None if stopped).
    - stop_event: threading.Event set() to interrupt immediately
    - on_detect: optional callback invoked with the recognized phrase
    Returns the phrase that triggered, or None if stopped.
    """
    model = _ensure_model()
    if model is None:
        print("[wake] Model unavailable; wake listening disabled.")
        return None

    print("VOX is sleeping... Say 'hey vox' to wake me up.")
    last_trigger = 0.0

    try:
        with sd.InputStream(samplerate=sample_rate, channels=1, dtype="float32") as stream:
            while not stop_event.is_set():
                # read N seconds of audio
                frames = int(sample_rate * window_sec)
                data, _ = stream.read(frames)
                if stop_event.is_set():
                    break

                # keep a little overlap for robustness
                buf = data
                if overlap_windows > 1:
                    more, _ = stream.read(frames)
                    buf = np.concatenate([data, more], axis=0)

                audio = np.squeeze(buf)  # (N,)
                # quick, low-beam transcription with VAD
                segments, _ = model.transcribe(
                    audio, beam_size=1, vad_filter=True, language="en"
                )
                phrase = " ".join(s.text for s in segments).strip().lower()

                if phrase and _heard_wake(phrase, threshold=threshold):
                    now = time.time()
                    if now - last_trigger < cooldown_sec:
                        continue
                    last_trigger = now
                    print("[wake] Detected phrase:", phrase)
                    if on_detect:
                        on_detect(phrase)
                    return phrase
    except KeyboardInterrupt:
        print("\n[wake] Stopped by user.")
    except Exception as e:
        print(f"[wake] Listener error: {e} (exiting)")

    return None


