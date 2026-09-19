# Laptop Automation Assistant 🚀

A lightweight, modular Windows desktop automation assistant built with Python.

This first version is a **text-command based** assistant designed to be simple, clean, and beginner-friendly. Voice recognition and advanced system controls can be plugged in naturally in future versions.

---

## 📁 Project Structure

```text
laptop-automation-assistant/
│
├── actions.py       # Functions that perform actions on your laptop (Chrome, WhatsApp, Search, Lock)
├── commands.py      # Parses user input and routes it to the correct action
├── main.py          # Interactive command-line loop (entry point)
└── README.md        # Documentation and guide
```

### What Each File Does:
1. **[actions.py](file:///C:/Users/Priyadarshan/OneDrive/Desktop/laptop-automation-assistant/actions.py)**: Contains the actual logic that interacts with Windows (using Python's built-in `os`, `ctypes`, `webbrowser`, and `urllib` modules). No external packages required!
2. **[commands.py](file:///C:/Users/Priyadarshan/OneDrive/Desktop/laptop-automation-assistant/commands.py)**: Takes what you type, cleans the text, matches it against known commands, and calls the appropriate function from `actions.py`.
3. **[main.py](file:///C:/Users/Priyadarshan/OneDrive/Desktop/laptop-automation-assistant/main.py)**: The main entry point. Starts the assistant, displays a prompt (`Assistant > `), and lets you interact continuously until you type `exit`.

---

## 💻 Supported Commands (v1.0)

| Command | What it does | Example |
|---|---|---|
| `help` | Shows the list of available commands | `help` |
| `open chrome` | Launches Google Chrome | `open chrome` |
| `open whatsapp` | Launches WhatsApp Desktop | `open whatsapp` |
| `search <query>` | Performs a Google search in your browser | `search python tutorial` |
| `lock` | Locks your Windows laptop (like Win + L) | `lock` |
| `exit` / `quit` | Closes the assistant | `exit` |

---

## 🚀 How to Run

1. Open PowerShell or Command Prompt in this folder (`laptop-automation-assistant`).
2. Run the application with Python:

```bash
python main.py
```

3. Type any command, for example:
```text
Assistant > search how to learn python
Searching Google for: 'how to learn python'

Assistant > open chrome
Opened Google Chrome.

Assistant > exit
Goodbye! Have a great day.
```

---

## 🛠️ How to Add a New Action (Beginner Guide)

Whenever you want to add a new command (for example, setting a timer or changing volume):

1. **Write the action logic in [actions.py](file:///C:/Users/Priyadarshan/OneDrive/Desktop/laptop-automation-assistant/actions.py)**:
   ```python
   def my_new_action() -> str:
       # Your logic here
       return "Action completed!"
   ```

2. **Route the command in [commands.py](file:///C:/Users/Priyadarshan/OneDrive/Desktop/laptop-automation-assistant/commands.py)**:
   - Add it to `AVAILABLE_COMMANDS` so `help` will show it.
   - Add a condition inside `process_command`:
     ```python
     if normalized == "my command":
         return actions.my_new_action(), True
     ```

3. **Run [main.py](file:///C:/Users/Priyadarshan/OneDrive/Desktop/laptop-automation-assistant/main.py)** and test your new command!
