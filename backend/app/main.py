from fastapi import FastAPI
from pydantic import BaseModel
import datetime
from app.voice import speak, listen
from app.commands import handle_command

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
    command = listen()
    return {"command": command}


@app.post("/speak")
def speak_route(request: CommandRequest):
    speak(request.text)
    return {"message": "Speaking"}


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
            speak("Note saved.")
            return {"response": "Note saved."}
        else:
            speak("Note cancelled.")
            return {"response": "Note cancelled."}

    if response:
        speak(response)

    return {"response": response}

