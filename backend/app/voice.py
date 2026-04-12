import pyttsx3
import threading
import queue
import json
import os
import sounddevice as sd
from vosk import Model, KaldiRecognizer

# ==========================
# TEXT TO SPEECH (STABLE)
# ==========================

engine = pyttsx3.init("sapi5")
engine.setProperty("rate", 170)
engine.setProperty("volume", 1.0)

voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)

# Queue system prevents crashes
tts_queue = queue.Queue()


def _tts_worker():
    """Single background thread handling ALL speech"""
    while True:
        text = tts_queue.get()
        try:
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print("❌ TTS Error:", e)


# Start worker ONCE
threading.Thread(target=_tts_worker, daemon=True).start()


def speak(text: str):
    """Non-blocking speech function"""
    if text:
        tts_queue.put(text)


# ==========================
# VOSK OFFLINE SPEECH MODEL
# ==========================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "..", "model")

if not os.path.exists(MODEL_PATH):
    raise Exception(f"Vosk model not found at: {MODEL_PATH}")

model = Model(MODEL_PATH)
recognizer = KaldiRecognizer(model, 16000)

audio_queue = queue.Queue()


def audio_callback(indata, frames, time, status):
    if status:
        print("Audio warning:", status)
    audio_queue.put(bytes(indata))


# ==========================
# LISTEN FUNCTION
# ==========================

def listen():
    """
    Offline speech recognition using Vosk.
    Blocks until a full command is detected.
    """

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
    """Useful for debugging mic issues"""
    import speech_recognition as sr
    return sr.Microphone.list_microphone_names()