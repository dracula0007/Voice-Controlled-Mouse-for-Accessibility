# 🎙️ Voice-Controlled Mouse for Accessibility

A Python-based voice-controlled mouse system designed to assist individuals with arm disabilities. This project leverages speech recognition and an intuitive graphical interface to perform common mouse and system tasks through voice commands.

## 📌 Features

- 🎤 **Real-time voice command recognition**
- 🖱️ **Mouse control via voice** (click, double-click, drag, move)
- 🪟 **Snap window support** (left, right, up, down, corners)
- 🧠 **Fuzzy matching for similar commands**
- 🔊 **Text-to-speech with robotic voice effect**
- 🧾 **Command history viewer**
- ⚙️ **Custom GUI with rounded edges**
- 🖼️ **Modern interface built with Tkinter and ttkbootstrap**

## 🛠️ Technologies Used

- Python 3.10+
- [Vosk](https://alphacephei.com/vosk/) for offline speech recognition
- `pyttsx3` for text-to-speech
- `pyautogui` for GUI automation
- `tkinter` and `ttkbootstrap` for GUI
- `difflib` for fuzzy command matching
- `pyinstaller` for packaging

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/dracula0007/Voice-Controlled-Mouse-for-Accessibility.git
cd Voice-Controlled-Mouse-for-Accessibility
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the app

```bash
python ZERO_GUI.py
```

## 📦 Build Executable (Optional)

Use `pyinstaller` to build the project into an `.exe`:

```bash
pyinstaller --onefile --windowed --icon=icon.ico --add-data "models;models" ZERO_GUI.py
```

> Make sure to include your model files, icons, and any dependencies in the packaging process.

## 🗣️ Voice Commands Supported

| Command        | Action                      |
|----------------|-----------------------------|
| `left click`   | Perform left mouse click    |
| `right click`  | Perform right mouse click   |
| `double click` | Perform double click        |
| `move up`      | Move mouse up               |
| `move down`    | Move mouse down             |
| `snap left`    | Snap window to the left     |
| `snap right`   | Snap window to the right    |
| `snap up`      | Snap window to the top      |
| `snap down`    | Snap window to the bottom   |
| `say`          | Speak out loud your input   |
| `exit`         | Close the application       |
| ...            | And more!                   |

## 🤝 Contribution

If you'd like to contribute, feel free to fork the repository and submit a pull request.

## 🧑‍🎓 Project Info

- **Project Type:** Graduation Project  
- **Domain:** Accessibility & AI

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
