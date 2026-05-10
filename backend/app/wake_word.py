import openwakeword
import sounddevice as sd
import numpy as np
import queue

class WakeWordListener:
    def __init__(self, on_wake_callback):
        self.on_wake_callback = on_wake_callback
        self.running = False

        # Load pre-trained model (comes with package)
        self.model = openwakeword.Model()

        self.audio_queue = queue.Queue()

    def start(self):
        self.running = True
        print("🟢 OpenWakeWord listening for 'jarvis'...")

        def audio_callback(indata, frames, time, status):
            self.audio_queue.put(indata.copy())

        stream = sd.InputStream(
            channels=1,
            samplerate=16000,
            callback=audio_callback
        )

        stream.start()

        while self.running:
            if not self.audio_queue.empty():
                audio = self.audio_queue.get()

                # Convert to float32
                audio = np.squeeze(audio)

                predictions = self.model.predict(audio)

                # Check if "jarvis" was detected
                if predictions.get("jarvis", 0) > 0.5:
                    print("🟡 Wake word detected: JARVIS!")
                    self.on_wake_callback()