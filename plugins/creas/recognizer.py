# core/recognizer.py

import sounddevice as sd
import numpy as np
import soundfile as sf
from faster_whisper import WhisperModel

# Load model (you can set to "base", "small", etc.)
model = WhisperModel("base.en", compute_type="int8", device="cpu")  # or "float32" if needed

def recognize_offline(duration=5, save_audio_path=None) -> str:
    print("\n🎤 Listening (speak now)...")

    fs = 16000
    try:
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float32')
        sd.wait()

        audio = np.squeeze(recording)

        # Save audio if path is given
        if save_audio_path:
            sf.write(save_audio_path, audio, fs)

        # Transcribe using faster-whisper
        segments, _ = model.transcribe(audio, beam_size=5)

        transcript = " ".join(segment.text for segment in segments).strip()

        if transcript:
            print(f"📝 Recognized: {transcript}")
            return transcript
        else:
            print("⚠️ No speech detected.")
            return None

    except Exception as e:
        print(f"❌ Recognition error: {e}")
        return None

