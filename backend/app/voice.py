import pyttsx3
import speech_recognition as sr
import threading

# ==========================
# GLOBAL RECOGNIZER (Reusable)
# ==========================
recognizer = sr.Recognizer()


# ==========================
# LISTEN FUNCTION
# ==========================
def listen(mic_index=None):
    """
    Captures audio from microphone and returns recognized text.
    Returns empty string if nothing detected or error occurs.
    """
    try:
        with sr.Microphone(device_index=mic_index) as source:
            recognizer.pause_threshold = 1
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=8
            )
    except sr.WaitTimeoutError:
        return ""
    except Exception:
        return ""

    try:
        command = recognizer.recognize_google(audio)
        return command.lower()
    except (sr.UnknownValueError, sr.RequestError):
        return ""


# ==========================
# SPEAK FUNCTION (Thread-safe)
# ==========================
def speak(text: str):
    """
    Runs TTS in a separate thread to prevent blocking FastAPI.
    """

    def tts():
        try:
            engine = pyttsx3.init("sapi5")
            voices = engine.getProperty("voices")
            engine.setProperty("voice", voices[0].id)
            engine.setProperty("rate", 170)
            engine.setProperty("volume", 1.0)
            engine.say(text)
            engine.runAndWait()
        except Exception:
            pass

    thread = threading.Thread(target=tts)
    thread.daemon = True
    thread.start()


# ==========================
# LIST MICROPHONES
# ==========================
def list_microphones():
    return sr.Microphone.list_microphone_names()

