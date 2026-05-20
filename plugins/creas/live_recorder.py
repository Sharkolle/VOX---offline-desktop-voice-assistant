# core/live_recorder.py

import sounddevice as sd
import soundfile as sf
import threading

class LiveRecorder:
    def __init__(self, samplerate=16000, channels=1):
        self.fs = samplerate
        self.channels = channels
        self.recording = False
        self.stream = None
        self.file = None
        self.thread = None
        self.file_path = None

    def start(self, filepath):
        self.file_path = filepath
        self.recording = True

        def callback(indata, frames, time, status):
            if status:
                print(f"⚠️ Stream status: {status}")
            if self.recording:
                self.file.write(indata)

        self.file = sf.SoundFile(
            filepath, mode='w', samplerate=self.fs,
            channels=self.channels, subtype='PCM_16'
        )

        self.stream = sd.InputStream(
            samplerate=self.fs,
            channels=self.channels,
            callback=callback
        )
        self.stream.start()
        print("🎙 Recording started...")

    def stop(self):
        self.recording = False
        if self.stream:
            self.stream.stop()
            self.stream.close()
        if self.file:
            self.file.close()
        print(f"🛑 Recording saved to {self.file_path}")
        return self.file_path
