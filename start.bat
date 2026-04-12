@echo off
echo Starting Jarvis...

:: Start backend (FastAPI)
cd backend
start cmd /k "py -3.11 -m uvicorn app.main:app --reload"

:: Wait a few seconds
timeout /t 5

:: Start Electron frontend
cd ..\electron
start cmd /k "npm start"

echo Jarvis started!
pause