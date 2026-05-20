from commands import speak, tell_date, tell_time
from core.voice_recognition import _recognize_offline

while True:
    print("say what you wnt me to write for you:\n")
    saved = _recognize_offline()
    with open("mynote", 'w') as f:
        f.write(saved)
        f.close()
