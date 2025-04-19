import queue
import sys
import sounddevice as sd
import vosk
import json
import pyautogui
import os
import signal
import time
import threading
import re
import pygetwindow as gw
import winsound
import webbrowser
import shutil
import difflib

import pyttsx3
import speech_recognition as sr

import help


# ✅ Set the model path relative to the script location
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_PATH, "D:\Graduation-Pro\ZEROv1.0.1\ZERO-model-small-en")

if not os.path.exists(MODEL_PATH):
    print(f"❌ Model not found at: {MODEL_PATH}")
    print("Please ensure the 'ZERO-model-small-en' folder is in the same directory as this application.")
    sys.exit(1)

model = vosk.Model(MODEL_PATH)

# ✅ Audio input settings
samplerate = 16000
blocksize = 8000
device = None
audio_queue = queue.Queue()

# ✅ Global variables
last_command = ""
recognizer = vosk.KaldiRecognizer(model, samplerate)
recognizer.SetWords(True)


# ✅ Say Command Setting
engine = pyttsx3.init()
engine.setProperty("rate", 140)
engine.setProperty("volume", 1.0)
voices = engine.getProperty("voices")
if len(voices) > 1:
    engine.setProperty("voice", voices[1].id)
else:
    engine.setProperty("voice", voices[0].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()


# ✅ Full command list with all original commands
COMMANDS = {
    "up": lambda: pyautogui.move(0, -40),
    "down": lambda: pyautogui.move(0, 40),
    "left": lambda: pyautogui.move(-40, 0),
    "right": lambda: pyautogui.move(40, 0),
    "move up": lambda: pyautogui.move(0, -150),     
    "move down": lambda: pyautogui.move(0, 150),
    "move left": lambda: pyautogui.move(-150, 0),
    "move right": lambda: pyautogui.move(150, 0),

    "click": lambda: pyautogui.click(),
    "double click": lambda: pyautogui.doubleClick(),
    "right click": lambda: pyautogui.rightClick(),
    "scroll up": lambda: pyautogui.scroll(100),
    "scroll down": lambda: pyautogui.scroll(-100),

    "open browser": lambda: open_app("chrome"),
    "file explorer": lambda: open_app("explorer"),
    "open notepad": lambda: open_app("notepad"),
    "settings": lambda: open_app("start ms-settings:"),
    "cmd": lambda: open_app("cmd"),
    "enter": lambda: (pyautogui.press("enter"), print("✅ Enter pressed!")),
    "delete character": lambda: (pyautogui.press("backspace"), print("✅ Deleted character!")),
    "task manager": lambda: open_app("taskmgr"),
    "open calculator": lambda: open_app("calc"),
    "open word": lambda: open_app("winword"),
    "open excel": lambda: open_app("excel"),

    "close window": lambda: (pyautogui.hotkey("alt", "f4"), print("✅ Window closed!")),
    "minimize window": lambda: (pyautogui.hotkey("win", "down"), print("✅ Window minimized!")),
    "maximize window": lambda: (pyautogui.hotkey("win", "up"), print("✅ Window maximized!")),
    "switch window": lambda: (pyautogui.hotkey("alt", "tab"), print("✅ Switched window!")),
    "show desktop": lambda: (pyautogui.hotkey("win", "d"), print("✅ Desktop shown!")),

    "snap left": lambda: (pyautogui.hotkey("win", "left"), print("✅ Snapped left!")),
    "snap right": lambda: (pyautogui.hotkey("win", "right"), print("✅ Snapped right!")),
    "snap up": lambda: (pyautogui.hotkey("win", "up"), print("✅ Snapped up!")),
    "snap down": lambda: (pyautogui.hotkey("win", "down"), print("✅ Snapped down!")),
    "snap top right": lambda: (pyautogui.hotkey("win", "right"), pyautogui.hotkey("win", "up"), print("✅ Snapped top right!")),
    "snap bottom right": lambda: (pyautogui.hotkey("win", "right"), pyautogui.hotkey("win", "down"), print("✅ Snapped bottom right!")),
    "snap top left": lambda: (pyautogui.hotkey("win", "left"), pyautogui.hotkey("win", "up"), print("✅ Snapped top left!")),
    "snap bottom left": lambda: (pyautogui.hotkey("win", "left"), pyautogui.hotkey("win", "down"), print("✅ Snapped bottom left!")),

    "play media": lambda: (pyautogui.press("playpause"), print("✅ Media played!")),
    "pause media": lambda: (pyautogui.press("playpause"), print("✅ Media paused!")),
    "next track": lambda: (pyautogui.press("nexttrack"), print("✅ Next track!")),
    "previous track": lambda: (pyautogui.press("prevtrack"), print("✅ Previous track!")),
    "volume up": lambda: (pyautogui.press("volumeup"), print("✅ Volume increased!")),
    "volume down": lambda: (pyautogui.press("volumedown"), print("✅ Volume decreased!")),
    "mute": lambda: (pyautogui.press("volumemute"), print("✅ Muted!")),

    "copy": lambda: (pyautogui.hotkey("ctrl", "c"), print("✅ Copied!")),
    "paste": lambda: (pyautogui.hotkey("ctrl", "v"), print("✅ Pasted!")),
    "cut": lambda: (pyautogui.hotkey("ctrl", "x"), print("✅ Cut!")),
    "delete": lambda: (pyautogui.press("delete"), print("✅ Deleted!")),
    "undo": lambda: (pyautogui.hotkey("ctrl", "z"), print("✅ Undone!")),
    "redo": lambda: (pyautogui.hotkey("ctrl", "y"), print("✅ Redone!")),
    "select all": lambda: (pyautogui.hotkey("ctrl", "a"), print("✅ Selected all!")),
    "type": lambda: write_text(),

    "new tab": lambda: (pyautogui.hotkey("ctrl", "t"), print("✅ New tab opened!")),
    "close tab": lambda: (pyautogui.hotkey("ctrl", "w"), print("✅ Tab closed!")),
    "refresh page": lambda: (pyautogui.hotkey("ctrl", "r"), print("✅ Page refreshed!")),
    "go back": lambda: (pyautogui.hotkey("alt", "left"), print("✅ Went back!")),
    "go forward": lambda: (pyautogui.hotkey("alt", "right"), print("✅ Went forward!")),
    "open google": lambda: (webbrowser.open("https://www.google.com"), print("✅ Google opened!")),
    "open youtube": lambda: (webbrowser.open("https://www.youtube.com"), print("✅ YouTube opened!")),

    "who developed you": lambda: (webbrowser.open("https://dracula0007.github.io/Portfolio"), print("✅ Great Man")),
    "how are you": lambda: engine.say("I'm fine, thank you for asking!") or engine.runAndWait(),
    "what is your name": lambda: engine.say("I'm ZERO 101, Developed to help people with disabilities use computers.!") or engine.runAndWait(),

    "create folder": lambda: create_folder(),
    "delete folder": lambda: delete_folder(),
    "open downloads": lambda: (os.startfile(os.path.expanduser("~/Downloads")), print("✅ Downloads opened!")),
    "open documents": lambda: (os.startfile(os.path.expanduser("~/Documents")), print("✅ Documents opened!")),

    "lock screen": lambda: (os.system("rundll32.exe user32.dll,LockWorkStation"), print("✅ Screen locked!")),
    "shut down": lambda: shutdown_with_confirmation(),
    "restart": lambda: (os.system("shutdown /r /t 0"), print("✅ Restarting!")),
    "sleep": lambda: (os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0"), print("✅ Sleeping!")),
    
    "new line": lambda: (pyautogui.press("enter"), print("✅ New line!")),
    "tab": lambda: (pyautogui.press("tab"), print("✅ Tab pressed!")),
    "space": lambda: (pyautogui.press("space"), print("✅ Space pressed!")),
    "capitalize": lambda: (pyautogui.hotkey("shift", pyautogui.press("right")), print("✅ Capitalized!")),
    "caps": lambda: (pyautogui.hotkey("capslock"), print("✅ Toggled uppercase!")),
    "fullscreen": lambda: (pyautogui.hotkey("f11"), print("✅ Fullscreen toggled!")),
    "take screenshot": lambda: take_screenshot(),
    "exit": lambda: (print("✅ Exiting program..."), os.kill(os.getpid(), signal.SIGTERM)),
}

# ✅ Function to open an application and move the mouse to its center
def open_app(zero):
    try:
        os.system(f"start {zero}")
        time.sleep(1)
        window = gw.getWindowsWithTitle(zero)[0]
        center_x = window.left + (window.width // 2)
        center_y = window.top + (window.height // 2)
        pyautogui.moveTo(center_x, center_y)
        print(f"✅ Mouse moved to the center of {zero}")
    except IndexError:
        print(f"❌ No window found for {zero}")
    except Exception as e:
        print(f"❌ Error opening {zero}: {e}")

# ✅ Function to create a folder
def create_folder():
    print("🎤 Please say the folder name...")
    folder_name = listen_for_text()
    if folder_name:
        try:
            os.makedirs(os.path.join(BASE_PATH, folder_name), exist_ok=True)
            print(f"✅ Folder created: {folder_name}")
        except Exception as e:
            print(f"❌ Error creating folder: {e}")
    else:
        print("❌ No folder name provided.")

# ✅ Function to delete a folder
def delete_folder():
    print("🎤 Please say the folder name to delete...")
    folder_name = listen_for_text()
    if folder_name:
        try:
            shutil.rmtree(os.path.join(BASE_PATH, folder_name), ignore_errors=True)
            print(f"✅ Folder deleted: {folder_name}")
        except Exception as e:
            print(f"❌ Error deleting folder: {e}")
    else:
        print("❌ No folder name provided.")

# ✅ Function to take a screenshot
def take_screenshot():
    try:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(BASE_PATH, f"screenshot_{timestamp}.png")
        pyautogui.screenshot(filename)
        print(f"✅ Screenshot saved as {filename}")
    except Exception as e:
        print(f"❌ Error taking screenshot: {e}")

# ✅ Function to write text
def write_text(text=None):
    if not text:
        print("🎤 Speak the text you want to write...")
        text = listen_for_text()
    if text:
        pyautogui.write(text)
        print(f"✅ Text written: {text}")
    else:
        print("❌ No text provided.")

# ✅ Function to listen for text with a timeout
def listen_for_text(timeout=10):
    start_time = time.time()
    while time.time() - start_time < timeout:
        data = audio_queue.get()
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())["text"]
            return clean_command(result)
    print("❌ No text recognized within timeout.")
    return ""

# ✅ Function to clean recognized text
def clean_command(text):
    if not text:
        return ""
    text = re.sub(r'\b(?:the|a|an)\b', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\s+', ' ', text).strip()
    return text
    

# ✅ Function for shutdown with confirmation
def shutdown_with_confirmation():
    print("🎤 Say 'yes' to confirm shutdown...")
    confirmation = listen_for_text()
    if confirmation.lower() == "yes":
        os.system("shutdown /s /t 0")
        print("✅ Shutting down...")
    else:
        print("❌ Shutdown canceled.")


# ✅ Main audio recognition function with improved handling
def recognize_audio():
    global last_command, recognizer
    print("🎤 Voice Control App is running... Speak now!")
    try:
        with sd.RawInputStream(samplerate=samplerate, blocksize=blocksize, device=device, dtype="int16",
                               channels=1, callback=callback) as stream:
            while True:
                data = audio_queue.get()
                if recognizer.AcceptWaveform(data):
                    result = json.loads(recognizer.Result())["text"]
                    cleaned_result = clean_command(result)
                    print(f"✅ Recognized: {result}")
                    print(f"🔧 Cleaned command: {cleaned_result}")

                    if cleaned_result == "say":
                        print("🤖 What should I say?")
                        # speak("What should I say?")

                        # time.sleep(1)
                        
                        #  Catch Voice For say command
                        while True:
                            data = audio_queue.get()
                            if recognizer.AcceptWaveform(data):
                                text_to_say = json.loads(recognizer.Result())["text"]
                                if text_to_say.strip():
                                    print(f"🔊 Robot says: {text_to_say}")
                                    speak(text_to_say)
                                    break
                        continue

                    if cleaned_result == "help":
                        print("ℹ️ Showing help...")
                        help.show_help()
                        continue
                    
                    if cleaned_result in COMMANDS:
                        print(f"✅ Executing command: {cleaned_result}")
                        COMMANDS[cleaned_result]()
                        play_sound()
                        last_command = cleaned_result
                    else:
                        closest_match = difflib.get_close_matches(cleaned_result, COMMANDS.keys(), n=1, cutoff=0.8)
                        if closest_match:
                            matched_command = closest_match[0]
                            print(f"✅ Fuzzy matched to: {matched_command}")
                            COMMANDS[matched_command]()
                            play_sound()
                            last_command = matched_command
                        elif cleaned_result == "exit":
                            print("✅ Exiting program...")
                            os.kill(os.getpid(), signal.SIGTERM)
                        else:
                            print("❌ Command not recognized.")
                            # play_sound(500, 200)
                    yield cleaned_result
                else:
                    partial = json.loads(recognizer.PartialResult())["partial"]
                    if partial and partial != last_partial():
                        print(f"🔍 Partial: {partial}")
                        last_partial(partial)
    except Exception as e:
        print(f"❌ Audio error: {e}. Please ensure a microphone is connected.")
        sys.exit(1)

# ✅ Helper to track last partial result
_last_partial = ""
def last_partial(value=None):
    global _last_partial
    if value is not None:
        _last_partial = value
    return _last_partial

# ✅ Function to play a sound
def play_sound(frequency=1000, duration=200):
    winsound.Beep(frequency, duration)

# ✅ Audio callback function
def callback(indata, frames, time_info, status):
    if status:
        print(f"⚠️ Audio status: {status}", file=sys.stderr)
    audio_queue.put(bytes(indata))

# ✅ Main execution
if __name__ == "__main__":
    print("✅ Voice Control Application Starting...")
    threading.Thread(target=recognize_audio, daemon=True).start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("✅ Program terminated by user.")
        sys.exit(0)