# Laptop Automation Assistant 🚀

A lightweight, modular Windows desktop automation assistant built with Python.

Supports both **text commands** and **voice input** using a unified, clean command routing architecture.

---

## 📁 Project Structure

```text
laptop-automation-assistant/
│
├── actions.py         # Low-level Windows automation (Apps, Volume, Battery, Search, Lock)
├── commands.py        # Parses text and routes both text and voice commands
├── voice.py           # Handles microphone input and speech recognition
├── main.py            # Interactive command-line loop (entry point)
├── run.bat            # One-click Windows batch launcher
├── requirements.txt   # Dependencies for voice input (SpeechRecognition, PyAudio)
├── .gitignore         # Prevents Python cache and system files from being tracked
└── README.md          # Documentation and guide
```

### What Each File Does:
1. **[actions.py](file:///C:/Users/Priyadarshan/OneDrive/Desktop/laptop-automation-assistant/actions.py)**: Low-level actions using Windows APIs and standard library (volume keys, power status, app execution).
2. **[commands.py](file:///C:/Users/Priyadarshan/OneDrive/Desktop/laptop-automation-assistant/commands.py)**: Central command processor. All inputs (text or voice) pass through here, ensuring no duplicated action logic.
3. **[voice.py](file:///C:/Users/Priyadarshan/OneDrive/Desktop/laptop-automation-assistant/voice.py)**: Encapsulates microphone listening and speech-to-text.
4. **[main.py](file:///C:/Users/Priyadarshan/OneDrive/Desktop/laptop-automation-assistant/main.py)**: The main entry point running the assistant loop.
5. **[run.bat](file:///C:/Users/Priyadarshan/OneDrive/Desktop/laptop-automation-assistant/run.bat)**: Double-clickable batch launcher for Windows.
6. **[requirements.txt](file:///C:/Users/Priyadarshan/OneDrive/Desktop/laptop-automation-assistant/requirements.txt)**: Lists the minimal packages needed for speech recognition.

---

## 💻 Supported Commands

| Command | What it does | Voice Example | Text Example |
|---|---|---|---|
| `voice` / `listen` | Listens to your microphone for a voice command | Speak into mic | `voice` |
| `volume up` | Increases system volume | "volume up" / "louder" | `volume up` |
| `volume down` | Decreases system volume | "volume down" / "quieter" | `volume down` |
| `mute` | Mutes system audio | "mute" / "mute volume" | `mute` |
| `unmute` | Unmutes system audio | "unmute" / "unmute audio" | `unmute` |
| `battery` | Reports battery level & charging state | "battery status" / "check battery" | `battery` |
| `open notepad` | Launches Windows Notepad | "open notepad" | `open notepad` |
| `open calculator` | Launches Windows Calculator | "open calculator" / "calc" | `open calculator` |
| `open file explorer` | Launches Windows File Explorer | "open file explorer" / "explorer" | `open file explorer` |
| `open settings` | Launches Windows Settings | "open settings" | `open settings` |
| `open youtube` | Opens YouTube in browser | "open youtube" | `open youtube` |
| `open chrome` | Launches Google Chrome | "open chrome" / "open google chrome" | `open chrome` |
| `open whatsapp` | Launches WhatsApp Desktop | "open whatsapp" | `open whatsapp` |
| `search <query>` | Performs a Google search in browser | "search for python" / "search python" | `search python tutorial` |
| `lock` | Locks your Windows laptop | "lock laptop" / "lock screen" | `lock` |
| `help` | Shows the list of available commands | "help" | `help` |
| `exit` / `quit` | Closes the assistant | "exit" / "bye" | `exit` |

---

## 🚀 Setup & Running

### 1. (Optional) Install Voice Dependencies
If you want to use the microphone for voice control:
```cmd
pip install -r requirements.txt
```
*(If you don't install these, text commands continue working normally as a fallback!)*

### 2. Run the Assistant
```cmd
python main.py
```

### 3. Using Voice Commands
When prompted with `Assistant > `, type `voice` or `listen`:
```text
Assistant > voice

[Voice Mode] Listening... (Speak your command into the microphone)
[Voice Mode] Processing speech...
[Voice Mode] Recognized: 'open chrome'
Opened Google Chrome.
```

If you prefer typing, simply type your command directly at any time:
```text
Assistant > search machine learning
Searching Google for: 'machine learning'
```
