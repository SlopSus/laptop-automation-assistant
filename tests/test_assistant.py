"""
test_assistant.py
-----------------
Automated test suite for Laptop Automation Assistant.
Covers:
- Text-to-Speech (TTS) engine, voice selection, and graceful error handling
- Natural spoken text formatting (JARVIS style)
- Command routing across all supported text commands and automations
- Voice STT integration routing

All audio playback is mocked or disabled during test execution.
"""

import unittest
from unittest.mock import MagicMock, patch
import os
import sys

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import actions
import commands
import voice
import tts


class TestTTSFormatting(unittest.TestCase):
    """Tests that display messages are transformed into natural, concise JARVIS-style speech."""

    def test_jarvis_required_phrases(self):
        """Verify the exact phrases specified in requirements."""
        # 1. Opening YouTube
        self.assertEqual(tts.get_spoken_text("Opened YouTube in browser."), "Opening YouTube.")

        # 2. Opening Chrome
        self.assertEqual(tts.get_spoken_text("Opened Google Chrome."), "Opening Chrome.")

        # 3. Battery status with charging
        self.assertEqual(
            tts.get_spoken_text("Battery: 85% | Status: Plugged in (Charging)"),
            "Your battery is 85 percent and charging.",
        )

        # 4. Volume increased
        self.assertEqual(tts.get_spoken_text("Volume increased."), "Volume increased.")

        # 5. Volume muted
        self.assertEqual(tts.get_spoken_text("Audio muted."), "Volume muted.")
        self.assertEqual(tts.get_spoken_text("Volume muted."), "Volume muted.")

        # 6. Unknown command
        unknown_msg = "Unknown command: 'xyz'.\nType 'help' to view the list of available commands."
        self.assertEqual(tts.get_spoken_text(unknown_msg), "I didn't understand that command.")

    def test_application_launchers(self):
        """Test spoken formatting for other application launchers."""
        self.assertEqual(tts.get_spoken_text("Opened WhatsApp."), "Opening WhatsApp.")
        self.assertEqual(tts.get_spoken_text("Opened Notepad."), "Opening Notepad.")
        self.assertEqual(tts.get_spoken_text("Opened Calculator."), "Opening Calculator.")
        self.assertEqual(tts.get_spoken_text("Opened File Explorer."), "Opening File Explorer.")
        self.assertEqual(tts.get_spoken_text("Opened Windows Settings."), "Opening Windows Settings.")

    def test_volume_and_system(self):
        """Test spoken formatting for volume and lock actions."""
        self.assertEqual(tts.get_spoken_text("Volume decreased."), "Volume decreased.")
        self.assertEqual(tts.get_spoken_text("Audio unmuted."), "Volume unmuted.")
        self.assertEqual(tts.get_spoken_text("Laptop locked successfully."), "Locking laptop.")

    def test_battery_variations(self):
        """Test battery on battery power and desktop AC power without battery."""
        self.assertEqual(
            tts.get_spoken_text("Battery: 50% | Status: Running on battery"),
            "Your battery is 50 percent and running on battery.",
        )
        self.assertEqual(
            tts.get_spoken_text("No battery detected. Laptop is running on AC power."),
            "No battery detected. Running on AC power.",
        )

    def test_search_and_meta_commands(self):
        """Test Google search, help menu, and exit formatting."""
        self.assertEqual(
            tts.get_spoken_text("Searching Google for: 'machine learning'"),
            "Searching Google for machine learning.",
        )
        self.assertEqual(
            tts.get_spoken_text(commands.get_help_message()),
            "Here are the available commands.",
        )
        self.assertEqual(
            tts.get_spoken_text("Goodbye! Have a great day."),
            "Goodbye! Have a great day.",
        )
        self.assertEqual(
            tts.get_spoken_text("Please enter a command. Type 'help' to see options."),
            "Please enter a command.",
        )

    def test_voice_stt_errors(self):
        """Test spoken responses for speech recognition failures."""
        self.assertEqual(
            tts.get_spoken_text("No speech detected within the timeout period. Returning to text mode."),
            "No speech detected.",
        )
        self.assertEqual(
            tts.get_spoken_text("Could not understand audio. Please speak clearly or use text mode."),
            "Could not understand audio.",
        )


class TestTTSEngineAndVoiceSelection(unittest.TestCase):
    """Tests voice selection heuristics, speech toggling, and exception handling."""

    def setUp(self):
        self.original_speech_state = tts.is_speech_enabled()

    def tearDown(self):
        tts.set_speech_enabled(self.original_speech_state)

    def test_speech_enabled_toggle(self):
        """Test enabling and disabling speech globally."""
        tts.set_speech_enabled(False)
        self.assertFalse(tts.is_speech_enabled())
        # When speech is disabled, speak() should immediately return False without calling engine
        self.assertFalse(tts.speak("Test speech disabled"))

        tts.set_speech_enabled(True)
        self.assertTrue(tts.is_speech_enabled())

    def test_speak_empty_text(self):
        """Test that empty or whitespace strings return False safely."""
        self.assertFalse(tts.speak(""))
        self.assertFalse(tts.speak("   "))
        self.assertFalse(tts.speak(None))

    def test_find_jarvis_voice_prefers_british(self):
        """Test that voice search prioritizes British voices when available."""
        mock_engine = MagicMock()
        mock_voices = [
            MagicMock(id="voice_david", name="Microsoft David Desktop", gender="Male"),
            MagicMock(id="voice_zira", name="Microsoft Zira Desktop", gender="Female"),
            MagicMock(id="voice_george", name="Microsoft George - English (United Kingdom)", gender="Male"),
        ]
        mock_engine.getProperty.return_value = mock_voices

        chosen = tts._find_jarvis_voice(mock_engine)
        self.assertEqual(chosen, "voice_george")

    def test_find_jarvis_voice_falls_back_to_david(self):
        """Test that voice search falls back to male voice (David) if no British voice is present."""
        mock_engine = MagicMock()
        mock_voices = [
            MagicMock(id="voice_zira", name="Microsoft Zira Desktop", gender="Female"),
            MagicMock(id="voice_david", name="Microsoft David Desktop", gender="Male"),
        ]
        mock_engine.getProperty.return_value = mock_voices

        chosen = tts._find_jarvis_voice(mock_engine)
        self.assertEqual(chosen, "voice_david")

    def test_speak_graceful_error_handling(self):
        """Test that engine exceptions during say() or runAndWait() do not crash the app."""
        tts.set_speech_enabled(True)
        with patch.object(tts, "_tts_engine") as mock_engine:
            mock_engine.say.side_effect = RuntimeError("Audio device busy")
            # Must return False gracefully without raising
            result = tts.speak("Hello world")
            self.assertFalse(result)

    def test_voice_module_exposes_tts(self):
        """Test that voice.py re-exports speak and get_spoken_text."""
        self.assertTrue(hasattr(voice, "speak"))
        self.assertTrue(hasattr(voice, "get_spoken_text"))
        self.assertIs(voice.speak, tts.speak)
        self.assertIs(voice.get_spoken_text, tts.get_spoken_text)


class TestCommandRouting(unittest.TestCase):
    """Verifies that all commands continue to route cleanly to actions."""

    def setUp(self):
        # Disable speech during command routing tests to avoid playing sound
        tts.set_speech_enabled(False)

    def tearDown(self):
        tts.set_speech_enabled(True)

    @patch("actions.volume_up", return_value="Volume increased.")
    def test_volume_up(self, mock_action):
        resp, keep_running = commands.process_command("volume up")
        self.assertEqual(resp, "Volume increased.")
        self.assertTrue(keep_running)
        mock_action.assert_called_once()

    @patch("actions.volume_down", return_value="Volume decreased.")
    def test_volume_down(self, mock_action):
        resp, keep_running = commands.process_command("volume down")
        self.assertEqual(resp, "Volume decreased.")
        self.assertTrue(keep_running)
        mock_action.assert_called_once()

    @patch("actions.mute_volume", return_value="Audio muted.")
    def test_mute_volume(self, mock_action):
        resp, keep_running = commands.process_command("mute")
        self.assertEqual(resp, "Audio muted.")
        self.assertTrue(keep_running)
        mock_action.assert_called_once()

    @patch("actions.unmute_volume", return_value="Audio unmuted.")
    def test_unmute_volume(self, mock_action):
        resp, keep_running = commands.process_command("unmute")
        self.assertEqual(resp, "Audio unmuted.")
        self.assertTrue(keep_running)
        mock_action.assert_called_once()

    @patch("actions.get_battery_status", return_value="Battery: 85% | Status: Plugged in (Charging)")
    def test_battery_status(self, mock_action):
        resp, keep_running = commands.process_command("battery")
        self.assertEqual(resp, "Battery: 85% | Status: Plugged in (Charging)")
        self.assertTrue(keep_running)
        mock_action.assert_called_once()

    @patch("actions.open_youtube", return_value="Opened YouTube in browser.")
    def test_open_youtube(self, mock_action):
        resp, keep_running = commands.process_command("open youtube")
        self.assertEqual(resp, "Opened YouTube in browser.")
        self.assertTrue(keep_running)
        mock_action.assert_called_once()

    @patch("actions.open_chrome", return_value="Opened Google Chrome.")
    def test_open_chrome(self, mock_action):
        resp, keep_running = commands.process_command("open chrome")
        self.assertEqual(resp, "Opened Google Chrome.")
        self.assertTrue(keep_running)
        mock_action.assert_called_once()

    @patch("actions.open_whatsapp", return_value="Opened WhatsApp.")
    def test_open_whatsapp(self, mock_action):
        resp, keep_running = commands.process_command("open whatsapp")
        self.assertEqual(resp, "Opened WhatsApp.")
        self.assertTrue(keep_running)
        mock_action.assert_called_once()

    @patch("actions.search_google", return_value="Searching Google for: 'python'")
    def test_search_google(self, mock_action):
        resp, keep_running = commands.process_command("search python")
        self.assertEqual(resp, "Searching Google for: 'python'")
        self.assertTrue(keep_running)
        mock_action.assert_called_once_with("python")

    @patch("actions.lock_windows", return_value="Laptop locked successfully.")
    def test_lock_windows(self, mock_action):
        resp, keep_running = commands.process_command("lock")
        self.assertEqual(resp, "Laptop locked successfully.")
        self.assertTrue(keep_running)
        mock_action.assert_called_once()

    def test_help_command(self):
        resp, keep_running = commands.process_command("help")
        self.assertIn("Available Commands:", resp)
        self.assertTrue(keep_running)

    def test_exit_command(self):
        resp, keep_running = commands.process_command("exit")
        self.assertIn("Goodbye!", resp)
        self.assertFalse(keep_running)

    def test_empty_command(self):
        resp, keep_running = commands.process_command("")
        self.assertIn("Please enter a command", resp)
        self.assertTrue(keep_running)

    def test_unknown_command(self):
        resp, keep_running = commands.process_command("unknown_xyz")
        self.assertIn("Unknown command", resp)
        self.assertTrue(keep_running)

    @patch("voice.listen_for_command", return_value=("open chrome", "Voice recognized: 'open chrome'"))
    @patch("actions.open_chrome", return_value="Opened Google Chrome.")
    def test_voice_command_flow(self, mock_open_chrome, mock_listen):
        resp, keep_running = commands.process_command("voice")
        self.assertEqual(resp, "Opened Google Chrome.")
        self.assertTrue(keep_running)
        mock_listen.assert_called_once()
        mock_open_chrome.assert_called_once()


if __name__ == "__main__":
    unittest.main()
