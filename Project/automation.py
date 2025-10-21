# automation.py
import webbrowser
import subprocess
import os
import platform
import pyautogui
from tts import speak

def open_website(url):
    webbrowser.open(url)

def open_app(app_name):
    """
    Attempts to open common apps. This is OS dependent.
    Provide basic cross-platform behavior:
    - On Windows: uses 'start' via shell
    - On macOS: uses 'open -a'
    - On Linux: tries xdg-open or the app name directly
    """
    plat = platform.system()
    try:
        if plat == "Windows":
            # Try startfile for full path; try shell start
            try:
                os.startfile(app_name)
                return True
            except Exception:
                subprocess.Popen(["start", app_name], shell=True)
                return True
        elif plat == "Darwin":
            subprocess.Popen(["open", "-a", app_name])
            return True
        else:
            # linux: try xdg-open or run app_name
            try:
                subprocess.Popen([app_name])
                return True
            except Exception:
                subprocess.Popen(["xdg-open", app_name])
                return True
    except Exception as e:
        speak(f"Unable to open {app_name}")
        print("open_app error:", e)
        return False

def take_screenshot(save_path="screenshot.png"):
    screenshot = pyautogui.screenshot()
    screenshot.save(save_path)
    speak(f"Saved screenshot to {save_path}")
    return save_path
