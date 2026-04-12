# Jarvis Desktop Assistant

Jarvis is a personal desktop voice assistant built with **Python** and **Electron**, designed to help you interact with your computer using voice commands.  
It can open apps, check system info, take notes, control volume, tell jokes, and more — all with a modern UI interface.

---

## Features

- Voice recognition using `SpeechRecognition`  
- Text-to-speech using `pyttsx3`  
- FastAPI backend providing a REST API  
- Electron frontend for a sleek desktop UI  
- Open apps and websites (Spotify, Chrome, VS Code, YouTube, Gmail)  
- System info & control (time, date, CPU/memory/battery, shutdown, restart, lock)  
- Take and save notes with timestamps  
- Take desktop screenshots  
- Fun commands like jokes  
- Easily extendable with new commands

---

## Project Structure

jarvis/
│
├── backend/ ← Python backend
│ ├── app/
│ │ ├── main.py ← FastAPI entry point
│ │ ├── voice.py ← Text-to-speech & speech-to-text functions
│ │ ├── commands.py ← Command handling logic
│ │ └── services.py ← Utility functions
│ │
│ └── requirements.txt ← Python dependencies
│
├── electron/ ← Electron frontend
│ ├── main.js ← Electron main process
│ ├── preload.js ← Secure bridge for API calls
│ ├── index.html ← UI layout
│ ├── renderer.js ← UI logic & event handling
│ └── package.json ← Node dependencies
│
└── README.md


---

## Setup

### 1. Install Python Dependencies

Make sure you have Python 3 installed. Then:

```bash
cd backend
python -m pip install -r requirements.txt


#Make sure node and npm are installed
node -v
npm -v

#Make sure electron is installed
cd ../electron
npm install

#Run app
npm run start