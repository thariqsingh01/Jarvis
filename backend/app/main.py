from fastapi import FastAPI
from pydantic import BaseModel
import datetime
from .voice import listen
from .commands import handle_command

app = FastAPI()


# ==========================
# Request Models
# ==========================
class CommandRequest(BaseModel):
    text: str


# ==========================
# Routes
# ==========================

@app.get("/")
def root():
    return {"status": "Jarvis API running"}


@app.post("/listen")
def listen_route():
    print("🔥 /listen called")
    command = listen()
    print("✅ heard:", command)
    return {"command": command}


@app.post("/speak")
def speak_route(request: CommandRequest):
    # kept for manual testing; frontend main flow uses this
    from .voice import speak
    duration = speak(request.text)
    return {"duration": duration}


@app.post("/command")
def command_route(request: CommandRequest):
    response = handle_command(request.text)

    if response is False:
        return {"shutdown": True}

    # Handle note logic here (backend responsibility now)
    if response == "Listening for note...":
        note_content = listen()
        if note_content:
            with open("jarvis_notes.txt", "a", encoding="utf-8") as f:
                f.write(f"[{datetime.datetime.now()}] {note_content}\n")
            # frontend handles TTS
            # speak("Note saved.")
            return {"response": "Note saved."}
        else:
            # frontend handles TTS
            # speak("Note cancelled.")
            return {"response": "Note cancelled."}

    # if response:
    #     speak(response)

    return {"response": response}

