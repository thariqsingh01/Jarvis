import os
import subprocess
import webbrowser
import datetime
import psutil
import random
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from PIL import ImageGrab


# ==========================
# VOLUME CONTROL
# ==========================
def set_volume(level):
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_,
            CLSCTX_ALL,
            None
        )
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMasterVolumeLevelScalar(level / 100, None)
        return f"Volume set to {level} percent."
    except Exception:
        return "Volume control failed."


# ==========================
# SAFE PROCESS KILLER
# ==========================
def kill_process_by_name(name):
    killed = False
    for process in psutil.process_iter(['name']):
        try:
            if process.info['name'] and name.lower() in process.info['name'].lower():
                process.kill()
                killed = True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return killed


# ==========================
# COMMAND HANDLER
# ==========================
def handle_command(cmd):
    """
    Returns:
        - string response
        - False if shutdown requested
        - True if no command
    """

    if not cmd:
        return True

    cmd = cmd.lower().strip()

    # ----------------------
    # Apps & Websites
    # ----------------------
    if "spotify" in cmd:
        os.system("start spotify:")
        return "Opening Spotify."

    elif "chrome" in cmd and "close" not in cmd:
        os.system("start chrome")
        return "Opening Google Chrome."

    elif "vscode" in cmd or "visual studio code" in cmd:
        subprocess.Popen("code", shell=True)
        return "Launching Visual Studio Code."

    elif "youtube" in cmd:
        webbrowser.open("https://youtube.com")
        return "Opening YouTube."

    elif "gmail" in cmd:
        webbrowser.open("https://mail.google.com")
        return "Opening Gmail."

    # ----------------------
    # System Info
    # ----------------------
    elif "time" in cmd:
        now = datetime.datetime.now().strftime("%I:%M %p")
        return f"The time is {now}"

    elif "date" in cmd:
        today = datetime.date.today().strftime("%B %d, %Y")
        return f"Today is {today}"

    elif "system report" in cmd:
        cpu = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory().percent
        battery = psutil.sensors_battery()

        if battery:
            return f"System report. CPU {cpu} percent. Memory {memory} percent. Battery {battery.percent} percent."
        else:
            return f"System report. CPU {cpu} percent. Memory {memory} percent. No battery detected."

    # ----------------------
    # System Control
    # ----------------------
    elif "lock computer" in cmd:
        os.system("rundll32.exe user32.dll,LockWorkStation")
        return "Locking workstation."

    elif "restart computer" in cmd:
        os.system("shutdown /r /t 5")
        return "Restarting in 5 seconds."

    elif "shutdown computer" in cmd:
        os.system("shutdown /s /t 5")
        return "Shutting down in 5 seconds."

    elif "set volume to" in cmd:
        try:
            level = int(''.join(filter(str.isdigit, cmd)))
            if 0 <= level <= 100:
                return set_volume(level)
            else:
                return "Please choose a level between 0 and 100."
        except:
            return "Volume level not understood."

    # ----------------------
    # Notes
    # ----------------------
    elif "take note" in cmd:
        return "Listening for note..."

    # ----------------------
    # Fun
    # ----------------------
    elif "joke" in cmd:
        jokes = [
            "Why do programmers prefer dark mode? Because light attracts bugs.",
            "Why was the computer cold? It forgot to close its Windows.",
            "Why did the AI cross the road? To optimize the other side.",
            "Why do Java developers wear glasses? Because they don't see sharp.",
            "I told my computer I needed a break. It said, no problem. I will go to sleep."
        ]
        return random.choice(jokes)

    # ----------------------
    # Close Apps
    # ----------------------
    elif "close chrome" in cmd:
        killed = kill_process_by_name("chrome")
        return "Chrome closed." if killed else "Chrome is not running."

    elif "close spotify" in cmd:
        killed = kill_process_by_name("spotify")
        return "Spotify closed." if killed else "Spotify is not running."

    # ----------------------
    # Screenshot
    # ----------------------
    elif "take screenshot" in cmd:
        path = os.path.join(os.environ["USERPROFILE"], "Desktop", "screenshot.png")
        ImageGrab.grab().save(path)
        return "Screenshot saved to desktop."

    # ----------------------
    # Exit
    # ----------------------
    elif "exit" in cmd or "quit" in cmd or "goodbye" in cmd:
        return False

    else:
        return "That function is not yet implemented."