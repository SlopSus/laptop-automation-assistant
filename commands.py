"""
commands.py
-----------
Interprets user input and routes it to the corresponding action in actions.py.
Separating command interpretation from execution keeps the code organized.
"""

from typing import Tuple
import actions
import voice

# List of supported commands for the help menu
AVAILABLE_COMMANDS = [
    ("voice / listen", "Listens for a voice command via microphone"),
    ("volume up", "Increases master volume"),
    ("volume down", "Decreases master volume"),
    ("mute", "Mutes system audio"),
    ("unmute", "Unmutes system audio"),
    ("battery", "Reports battery percentage and charging status"),
    ("open notepad", "Opens Windows Notepad"),
    ("open calculator", "Opens Windows Calculator"),
    ("open file explorer", "Opens Windows File Explorer"),
    ("open settings", "Opens Windows Settings"),
    ("open youtube", "Opens YouTube in default browser"),
    ("open chrome", "Opens the Google Chrome browser"),
    ("open whatsapp", "Opens WhatsApp Desktop"),
    ("search <query>", "Searches Google for the given keywords (e.g., search python)"),
    ("lock", "Locks the Windows laptop screen"),
    ("help", "Displays this list of available commands"),
    ("exit / quit", "Closes the Laptop Automation Assistant"),
]


def get_help_message() -> str:
    """Returns a formatted string listing all supported commands."""
    lines = ["Available Commands:"]
    for cmd, desc in AVAILABLE_COMMANDS:
        lines.append(f"  - {cmd:<20} : {desc}")
    return "\n".join(lines)


def process_command(user_input: str) -> Tuple[str, bool]:
    """
    Parses the user's text input and invokes the appropriate action.

    Parameters:
        user_input (str): The raw text entered by the user.

    Returns:
        tuple (str, bool):
            - str: The response message to display to the user.
            - bool: True to keep the assistant running, False to exit.
    """
    text = user_input.strip()

    # If the user pressed enter without typing anything
    if not text:
        return "Please enter a command. Type 'help' to see options.", True

    normalized = text.lower()

    # --- Exit Commands ---
    if normalized in ("exit", "quit", "q", "bye", "exit assistant", "close assistant"):
        return "Goodbye! Have a great day.", False

    # --- Help Command ---
    if normalized in ("help", "commands", "?"):
        return get_help_message(), True

    # --- Voice Input Trigger ---
    if normalized in ("voice", "listen", "v", "mic"):
        recognized_text, status = voice.listen_for_command()
        if not recognized_text:
            return status, True
        print(f"[Voice Mode] Recognized: '{recognized_text}'")
        # Route recognized speech directly through this same command processor!
        return process_command(recognized_text)

    # --- Volume Controls ---
    if normalized in ("volume up", "increase volume", "turn volume up", "turn up volume", "raise volume", "louder"):
        return actions.volume_up(), True

    if normalized in ("volume down", "decrease volume", "turn volume down", "turn down volume", "lower volume", "quieter"):
        return actions.volume_down(), True

    if normalized in ("mute", "mute volume", "mute audio", "silence"):
        return actions.mute_volume(), True

    if normalized in ("unmute", "unmute volume", "unmute audio"):
        return actions.unmute_volume(), True

    # --- Battery Status ---
    if normalized in (
        "battery",
        "battery status",
        "battery percentage",
        "battery level",
        "check battery",
        "power status",
        "how much battery",
    ):
        return actions.get_battery_status(), True

    # --- Quick Application Launchers ---
    if normalized in ("open notepad", "notepad", "launch notepad"):
        return actions.open_notepad(), True

    if normalized in ("open calculator", "open calc", "calculator", "calc", "launch calculator"):
        return actions.open_calculator(), True

    if normalized in (
        "open file explorer",
        "open explorer",
        "file explorer",
        "explorer",
        "open files",
        "launch explorer",
    ):
        return actions.open_file_explorer(), True

    if normalized in (
        "open settings",
        "open windows settings",
        "settings",
        "windows settings",
        "launch settings",
    ):
        return actions.open_settings(), True

    if normalized in ("open youtube", "youtube", "launch youtube"):
        return actions.open_youtube(), True

    # --- Open Chrome ---
    if normalized in ("open chrome", "chrome", "launch chrome", "open google chrome"):
        return actions.open_chrome(), True

    # --- Open WhatsApp ---
    if normalized in ("open whatsapp", "whatsapp", "launch whatsapp", "open the whatsapp"):
        return actions.open_whatsapp(), True

    # --- Lock Windows ---
    if normalized in (
        "lock",
        "lock laptop",
        "lock windows",
        "lock screen",
        "lock the laptop",
        "lock my laptop",
        "lock computer",
    ):
        return actions.lock_windows(), True

    # --- Search Google ---
    # Matches "search <query>", "search for <query>", "search google <query>", or "google <query>"
    if normalized.startswith("search google "):
        query = text[len("search google "):]
        return actions.search_google(query), True
    elif normalized.startswith("search for "):
        query = text[len("search for "):]
        return actions.search_google(query), True
    elif normalized.startswith("search "):
        query = text[len("search "):]
        return actions.search_google(query), True
    elif normalized.startswith("google "):
        query = text[len("google "):]
        return actions.search_google(query), True

    # Unrecognized command
    return (
        f"Unknown command: '{text}'.\n"
        "Type 'help' to view the list of available commands."
    ), True
