@echo off
echo Starting Jarvis...

:: Go to project root (important for reliability)
cd /d %~dp0

:: Activate virtual environment
call venv\Scripts\activate

:: Start backend (FastAPI inside venv)
echo Starting FastAPI backend...
start cmd /k "cd backend && python -m uvicorn app.main:app --reload"

:: Wait for backend to initialize
timeout /t 5 >nul

:: Start Electron frontend
echo Starting Electron frontend...
start cmd /k "cd electron && npm start"

echo Jarvis started successfully!
pause