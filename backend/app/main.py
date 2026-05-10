from fastapi import FastAPI
from pydantic import BaseModel
from contextlib import asynccontextmanager
import asyncio
import datetime

from .voice import listen, speak
from .commands import handle_command
from .wake_word import WakeWordListener


# ==========================
# Globals
# ==========================
wake_listener = None
listening_lock = False


# ==========================
# Request Models
# ==========================
class CommandRequest(BaseModel):
    text: str


# ==========================
# Core Logic
# ==========================
def activate_jarvis():
    global listening_lock

    # Prevent mic conflicts
    if listening_lock:
        return

    listening_lock = True
    print("⚡ Jarvis activated!")

    try:
        text = listen()

        if text:
            handle_command(text)

    finally:
        listening_lock = False


# ==========================
# Lifespan (startup/shutdown)
# ==========================
@asynccontextmanager
async def lifespan(app: FastAPI):
    global wake_listener

    # STARTUP
    wake_listener = WakeWordListener(on_wake_callback=activate_jarvis)

    # Run wake word listener in background thread safely
    loop = asyncio.get_event_loop()
    task = loop.run_in_executor(None, wake_listener.start)

    print("🟢 Jarvis backend started with wake word listener")

    yield  # App runs here

    # SHUTDOWN
    print("🔴 Shutting down Jarvis...")

    await wake_listener.stop()


# ==========================
# App
# ==========================
app = FastAPI(lifespan=lifespan)


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
    duration = speak(request.text)
    return {"duration": duration}


@app.post("/command")
def command_route(request: CommandRequest):
    response = handle_command(request.text)

    if response is False:
        return {"shutdown": True}

    # Special note mode
    if response == "Listening for note...":
        note_content = listen()

        if note_content:
            with open("jarvis_notes.txt", "a", encoding="utf-8") as f:
                f.write(f"[{datetime.datetime.now()}] {note_content}\n")

            return {"response": "Note saved."}
        else:
            return {"response": "Note cancelled."}

    return {"response": response}