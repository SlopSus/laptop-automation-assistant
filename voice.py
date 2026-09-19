"""
voice.py
--------
Handles audio capture and speech-to-text recognition.
Converts spoken words into text commands using the SpeechRecognition library.
"""

from typing import Tuple, Optional

try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    sr = None
    SPEECH_RECOGNITION_AVAILABLE = False


def is_speech_recognition_available() -> bool:
    """Returns True if SpeechRecognition library is installed, False otherwise."""
    return SPEECH_RECOGNITION_AVAILABLE


def listen_for_command(timeout: int = 5, phrase_time_limit: int = 7) -> Tuple[Optional[str], str]:
    """
    Listens to the microphone and converts speech to text.

    Parameters:
        timeout (int): Seconds to wait for the user to start speaking.
        phrase_time_limit (int): Maximum seconds allowed for the spoken phrase.

    Returns:
        tuple (Optional[str], str):
            - Optional[str]: The recognized text command, or None if failed.
            - str: A human-readable status message.
    """
    if not SPEECH_RECOGNITION_AVAILABLE:
        return None, (
            "Speech recognition library not found.\n"
            "Please install it by running: pip install -r requirements.txt"
        )

    recognizer = sr.Recognizer()

    try:
        # Check for microphone availability
        with sr.Microphone() as source:
            print("\n[Voice Mode] Listening... (Speak your command into the microphone)")
            # Calibrate for ambient background noise to improve recognition quality
            recognizer.adjust_for_ambient_noise(source, duration=0.8)
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)

        print("[Voice Mode] Processing speech...")
        # Use Google's free speech recognition API to convert audio to text
        recognized_text = recognizer.recognize_google(audio)
        return recognized_text, f"Voice recognized: '{recognized_text}'"

    except sr.WaitTimeoutError:
        return None, "No speech detected within the timeout period. Returning to text mode."
    except sr.UnknownValueError:
        return None, "Could not understand audio. Please speak clearly or use text mode."
    except sr.RequestError as error:
        return None, f"Speech recognition service error: {error}"
    except (OSError, AttributeError) as error:
        return None, f"Microphone error: {error}. Please ensure a microphone is connected."
    except Exception as error:
        return None, f"Unexpected error during speech recognition: {error}"
