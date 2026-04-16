import pyttsx3
import threading
import queue
import json
import os
import sounddevice as sd
from vosk import Model, KaldiRecognizer

# ==========================
# TTS (FIXED - SAFE FOR WINDOWS)
# ==========================

def speak(text: str):
    """
    Safe non-blocking TTS.
    Creates a fresh engine per call to avoid SAPI5 lockups.
    """

    def run():
        try:
            engine = pyttsx3.init("sapi5")
            engine.setProperty("rate", 170)
            engine.setProperty("volume", 1.0)

            voices = engine.getProperty("voices")
            engine.setProperty("voice", voices[0].id)

            engine.say(text)
            engine.runAndWait()
            engine.stop()

        except Exception as e:
            print("❌ TTS Error:", e)

    threading.Thread(target=run, daemon=True).start()


# ==========================
# VOSK SETUP
# ==========================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "..", "model")

if not os.path.exists(MODEL_PATH):
    raise Exception(f"Vosk model not found at: {MODEL_PATH}")

model = Model(MODEL_PATH)

audio_queue = queue.Queue()


def audio_callback(indata, frames, time, status):
    if status:
        print("Audio warning:", status)
    audio_queue.put(bytes(indata))


# ==========================
# LISTEN FUNCTION (FIXED)
# ==========================

def listen():
    """
    Offline speech recognition using Vosk.
    Clean reset every call to prevent "works once" bug.
    """

    # 🔥 IMPORTANT FIX 1: reset recognizer every call
    recognizer = KaldiRecognizer(model, 16000)

    # 🔥 IMPORTANT FIX 2: clear old audio chunks
    while not audio_queue.empty():
        audio_queue.get()

    try:
        with sd.RawInputStream(
            samplerate=16000,
            blocksize=8000,
            dtype="int16",
            channels=1,
            callback=audio_callback
        ):

            print("🎤 Listening offline...")

            while True:
                data = audio_queue.get()

                if recognizer.AcceptWaveform(data):
                    result = json.loads(recognizer.Result())
                    text = result.get("text", "").strip()

                    if text:
                        print("🧠 Recognized:", text)
                        return text.lower()

    except Exception as e:
        print("❌ Listen Error:", e)
        return ""


# ==========================
# MICROPHONE DEBUG TOOL
# ==========================

def list_microphones():
    import speech_recognition as sr
    return sr.Microphone.list_microphone_names()