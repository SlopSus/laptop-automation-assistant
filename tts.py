"""
tts.py
------
Handles Text-to-Speech (TTS) synthesis for Laptop Automation Assistant.
Configured with a JARVIS-inspired profile:
- Calm, steady, professional delivery (~160 WPM)
- Deep/clear voice selection (prioritizes British English voice if installed,
  otherwise defaults to a calm male voice like Microsoft David)
- Safe error handling so audio failures never break assistant execution
- Automatic translation from terminal status output to natural spoken dialogue
"""

import re
from typing import Optional

try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    pyttsx3 = None
    PYTTSX3_AVAILABLE = False


# Module-level settings and cached engine instance
_tts_engine = None
_tts_initialized = False
_speech_enabled = True


def is_tts_available() -> bool:
    """Returns True if a TTS engine is available and functional."""
    _ensure_engine_initialized()
    return _tts_engine is not None


def set_speech_enabled(enabled: bool) -> None:
    """
    Enables or disables speech output globally.
    Useful for testing or running in headless/quiet environments.
    """
    global _speech_enabled
    _speech_enabled = enabled


def is_speech_enabled() -> bool:
    """Returns True if speech output is currently enabled."""
    return _speech_enabled


def _find_jarvis_voice(engine) -> Optional[str]:
    """
    Searches installed system voices for the best match fitting a JARVIS persona:
    1. British English voice (e.g., George, Hazel, Oliver, Susan, en-GB).
    2. Deep/calm male voice (e.g., David, Mark).
    3. First available system voice.
    """
    try:
        voices = engine.getProperty("voices")
        if not voices:
            return None

        # Priority 1: British English male voice
        for voice in voices:
            v_name = (getattr(voice, "name", "") or "").lower()
            v_id = (getattr(voice, "id", "") or "").lower()
            is_british = any(k in v_name or k in v_id for k in ("en-gb", "uk", "british", "george", "hazel", "oliver"))
            is_male = any(k in v_name or k in v_id for k in ("male", "david", "mark", "george", "oliver")) or getattr(voice, "gender", "") == "Male"
            if is_british and is_male:
                return voice.id

        # Priority 2: Any British English voice
        for voice in voices:
            v_name = (getattr(voice, "name", "") or "").lower()
            v_id = (getattr(voice, "id", "") or "").lower()
            if any(k in v_name or k in v_id for k in ("en-gb", "uk", "british", "george", "hazel", "susan", "oliver")):
                return voice.id

        # Priority 3: Deep / calm male voice (e.g. David)
        for voice in voices:
            v_name = (getattr(voice, "name", "") or "").lower()
            v_id = (getattr(voice, "id", "") or "").lower()
            if any(k in v_name or k in v_id for k in ("david", "mark", "male")) or getattr(voice, "gender", "") == "Male":
                return voice.id

        # Fallback: Default to the first voice in the system list
        return voices[0].id
    except Exception:
        return None


def _ensure_engine_initialized() -> None:
    """Initializes the pyttsx3 speech engine once and configures voice parameters."""
    global _tts_engine, _tts_initialized

    if _tts_engine is not None or _tts_initialized:
        return

    _tts_initialized = True

    if not PYTTSX3_AVAILABLE:
        return

    try:
        engine = pyttsx3.init()

        # Select the best voice fitting the JARVIS profile
        selected_voice = _find_jarvis_voice(engine)
        if selected_voice:
            try:
                engine.setProperty("voice", selected_voice)
            except Exception:
                pass

        # Set speech rate: 160 WPM (calm, steady, professional delivery)
        # Default 200 WPM is rushed; 160 WPM gives a composed assistant demeanor
        try:
            engine.setProperty("rate", 160)
        except Exception:
            pass

        # Set volume: full clarity
        try:
            engine.setProperty("volume", 1.0)
        except Exception:
            pass

        _tts_engine = engine
    except Exception:
        _tts_engine = None


def get_spoken_text(display_message: str) -> str:
    """
    Transforms raw terminal status output into clean, natural spoken phrases
    fitting a JARVIS-style assistant.

    Examples:
        - "Opened YouTube in browser." -> "Opening YouTube."
        - "Opened Google Chrome." -> "Opening Chrome."
        - "Volume increased." -> "Volume increased."
        - "Audio muted." -> "Volume muted."
        - "Battery: 85% | Status: Plugged in (Charging)" -> "Your battery is 85 percent and charging."
        - "Unknown command: 'foo'..." -> "I didn't understand that command."
        - Multi-line help output -> "Here are the available commands."
    """
    if not display_message:
        return ""

    cleaned = display_message.strip()

    # --- Application Launches ---
    if cleaned == "Opened YouTube in browser.":
        return "Opening YouTube."
    if cleaned == "Opened Google Chrome.":
        return "Opening Chrome."
    if cleaned == "Opened WhatsApp.":
        return "Opening WhatsApp."
    if cleaned == "Opened Notepad.":
        return "Opening Notepad."
    if cleaned == "Opened Calculator.":
        return "Opening Calculator."
    if cleaned == "Opened File Explorer.":
        return "Opening File Explorer."
    if cleaned == "Opened Windows Settings.":
        return "Opening Windows Settings."

    # --- Volume Control ---
    if cleaned == "Volume increased.":
        return "Volume increased."
    if cleaned == "Volume decreased.":
        return "Volume decreased."
    if cleaned in ("Audio muted.", "Volume muted."):
        return "Volume muted."
    if cleaned in ("Audio unmuted.", "Volume unmuted."):
        return "Volume unmuted."

    # --- Battery Status ---
    if cleaned.startswith("Battery:"):
        match = re.search(r"Battery:\s*(\d+)%\s*\|\s*Status:\s*(.+)", cleaned)
        if match:
            percent, raw_status = match.group(1), match.group(2).lower()
            if "charging" in raw_status:
                return f"Your battery is {percent} percent and charging."
            elif "running on battery" in raw_status or "battery" in raw_status:
                return f"Your battery is {percent} percent and running on battery."
            else:
                return f"Your battery is at {percent} percent."
        return "Battery status checked."

    if "no battery detected" in cleaned.lower():
        return "No battery detected. Running on AC power."

    # --- System Lock ---
    if cleaned == "Laptop locked successfully.":
        return "Locking laptop."

    # --- Google Search ---
    search_match = re.search(r"^Searching Google for:\s*['\"]?(.*?)['\"]?$", cleaned)
    if search_match:
        query = search_match.group(1).strip()
        if query:
            return f"Searching Google for {query}."
        return "Searching Google."

    # --- Unknown / Error Commands ---
    if cleaned.startswith("Unknown command:"):
        return "I didn't understand that command."

    # --- Help Menu (avoid speaking lengthy multi-line table) ---
    if cleaned.startswith("Available Commands:"):
        return "Here are the available commands."

    # --- Empty Prompt ---
    if cleaned.startswith("Please enter a command"):
        return "Please enter a command."

    # --- Exit ---
    if cleaned.startswith("Goodbye!"):
        return "Goodbye! Have a great day."

    # --- Voice STT Errors ---
    if cleaned.startswith("No speech detected"):
        return "No speech detected."
    if cleaned.startswith("Could not understand audio"):
        return "Could not understand audio."

    # Fallback: clean any newlines and extra spaces
    first_line = cleaned.split("\n")[0].strip()
    return first_line


def speak(text: str) -> bool:
    """
    Speaks the given text aloud using the configured TTS engine.

    Parameters:
        text (str): The sentence to vocalize.

    Returns:
        bool: True if speech completed successfully, False otherwise.
    """
    if not _speech_enabled:
        return False

    if not text or not text.strip():
        return False

    _ensure_engine_initialized()

    if _tts_engine is None:
        return False

    try:
        _tts_engine.say(text)
        _tts_engine.runAndWait()
        return True
    except Exception:
        # Gracefully swallow errors so TTS issues never crash the main application
        return False
