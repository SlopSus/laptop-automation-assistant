# Laptop Automation Assistant 🚀

A lightweight, modular Windows desktop automation assistant built with Python.

Supports both **text commands** and **voice input** using a unified, clean command routing architecture.

---

## 📁 Project Structure

```text
laptop-automation-assistant/
│
├── actions.py         # Low-level functions that interact with Windows (Chrome, WhatsApp, Search, Lock)
├── commands.py        # Parses text and routes both text and voice commands
├── voice.py           # Handles microphone input and speech recognition
├── main.py            # Interactive command-line loop (entry point)
├── requirements.txt   # Dependencies for voice input (SpeechRecognition, PyAudio)
├── .gitignore         # Prevents Python cache and system files from being tracked
└── README.md          # Documentation and guide
```

### What Each File Does:
1. **[actions.py](file:///C:/Users/Priyadarshan/OneDrive/Desktop/laptop-automation-assistant/actions.py)**: Low-level actions (uses Windows APIs and standard library).
2. **[commands.py](file:///C:/Users/Priyadarshan/OneDrive/Desktop/laptop-automation-assistant/commands.py)**: Central command processor. All inputs (text or voice) pass through here, ensuring no duplicated action logic.
3. **[voice.py](file:///C:/Users/Priyadarshan/OneDrive/Desktop/laptop-automation-assistant/voice.py)**: Encapsulates microphone listening and speech-to-text.
4. **[main.py](file:///C:/Users/Priyadarshan/OneDrive/Desktop/laptop-automation-assistant/main.py)**: The main entry point running the assistant loop.
5. **[requirements.txt](file:///C:/Users/Priyadarshan/OneDrive/Desktop/laptop-automation-assistant/requirements.txt)**: Lists the minimal packages needed for speech recognition.

---

## 💻 Supported Commands

| Command | What it does | Voice Example | Text Example |
|---|---|---|---|
| `voice` / `listen` | Listens to your microphone for a voice command | Speak into mic | `voice` |
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
