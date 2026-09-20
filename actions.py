"""
actions.py
----------
Contains all the core automation functions that interact with Windows.
Each function is responsible for a single action, keeping the logic modular.
Uses only Python's built-in standard library (no external packages required).
"""

import os
import ctypes
import webbrowser
import urllib.parse
import subprocess


def open_chrome() -> str:
    """
    Opens the Google Chrome browser.
    Returns a status message indicating success or failure.
    """
    try:
        # os.startfile asks Windows to launch the program via Windows App Paths
        os.startfile("chrome")
        return "Opened Google Chrome."
    except Exception:
        # Fallback in case os.startfile cannot locate 'chrome' directly
        try:
            subprocess.Popen(["cmd", "/c", "start", "chrome"], shell=False)
            return "Opened Google Chrome."
        except Exception as error:
            return f"Could not open Chrome: {error}"


def open_whatsapp() -> str:
    """
    Opens WhatsApp using the Windows protocol handler ('whatsapp:').
    Returns a status message indicating success or failure.
    """
    try:
        # WhatsApp Desktop registers the 'whatsapp:' URI scheme in Windows
        os.startfile("whatsapp:")
        return "Opened WhatsApp."
    except Exception as error:
        return f"Could not open WhatsApp: {error}"


def search_google(query: str) -> str:
    """
    Performs a Google search in the default web browser.

    Parameters:
        query (str): The search term entered by the user.

    Returns:
        str: Status message confirming the search.
    """
    cleaned_query = query.strip()
    if not cleaned_query:
        return "Please enter something to search. Example: 'search python tutorial'"

    # urllib.parse.quote_plus safely encodes spaces and special characters into URL format
    encoded_query = urllib.parse.quote_plus(cleaned_query)
    url = f"https://www.google.com/search?q={encoded_query}"

    # webbrowser.open opens the URL in the system's default browser
    webbrowser.open(url)
    return f"Searching Google for: '{cleaned_query}'"


def lock_windows() -> str:
    """
    Locks the Windows workstation (equivalent to pressing Win + L).
    Returns a status message.
    """
    try:
        # ctypes allows calling native C functions in Windows DLLs
        # user32.dll provides the LockWorkStation function
        ctypes.windll.user32.LockWorkStation()
        return "Laptop locked successfully."
    except Exception as error:
        return f"Could not lock laptop: {error}"


# Virtual-Key codes for Windows multimedia keys in user32.dll
VK_VOLUME_MUTE = 0xAD
VK_VOLUME_DOWN = 0xAE
VK_VOLUME_UP = 0xAF
KEYEVENTF_KEYUP = 0x0002


def _press_key(vk_code: int, times: int = 1) -> None:
    """Simulates pressing and releasing a virtual key in Windows."""
    for _ in range(times):
        ctypes.windll.user32.keybd_event(vk_code, 0, 0, 0)
        ctypes.windll.user32.keybd_event(vk_code, 0, KEYEVENTF_KEYUP, 0)


def volume_up(steps: int = 5) -> str:
    """
    Increases system master volume.
    Each key press corresponds to ~2% volume increment in Windows.
    """
    try:
        _press_key(VK_VOLUME_UP, steps)
        return "Volume increased."
    except Exception as error:
        return f"Could not increase volume: {error}"


def volume_down(steps: int = 5) -> str:
    """
    Decreases system master volume.
    Each key press corresponds to ~2% volume decrement in Windows.
    """
    try:
        _press_key(VK_VOLUME_DOWN, steps)
        return "Volume decreased."
    except Exception as error:
        return f"Could not decrease volume: {error}"


def mute_volume() -> str:
    """
    Mutes system audio output.
    """
    try:
        _press_key(VK_VOLUME_MUTE, 1)
        return "Audio muted."
    except Exception as error:
        return f"Could not mute volume: {error}"


def unmute_volume() -> str:
    """
    Unmutes system audio output.
    In Windows, sending Volume Up automatically unmutes the system,
    and sending Volume Down immediately restores the original volume level.
    """
    try:
        _press_key(VK_VOLUME_UP, 1)
        _press_key(VK_VOLUME_DOWN, 1)
        return "Audio unmuted."
    except Exception as error:
        return f"Could not unmute volume: {error}"


class _SYSTEM_POWER_STATUS(ctypes.Structure):
    """Windows C structure representing system power and battery status."""
    _fields_ = [
        ("ACLineStatus", ctypes.c_byte),
        ("BatteryFlag", ctypes.c_byte),
        ("BatteryLifePercent", ctypes.c_ubyte),
        ("SystemStatusFlag", ctypes.c_byte),
        ("BatteryLifeTime", ctypes.c_ulong),
        ("BatteryFullLifeTime", ctypes.c_ulong),
    ]


def get_battery_status() -> str:
    """
    Retrieves the laptop battery percentage and power/charging state
    using the Windows kernel32.GetSystemPowerStatus API.
    """
    try:
        status = _SYSTEM_POWER_STATUS()
        if not ctypes.windll.kernel32.GetSystemPowerStatus(ctypes.byref(status)):
            return "Could not retrieve battery status."

        # BatteryFlag 128 indicates no battery is installed (e.g. desktop PC)
        if status.BatteryFlag == 128:
            return "No battery detected. Laptop is running on AC power."

        percent = status.BatteryLifePercent
        percent_str = f"{percent}%" if percent != 255 else "Unknown"

        if status.ACLineStatus == 1:
            charging_state = "Plugged in (Charging)"
        elif status.ACLineStatus == 0:
            charging_state = "Running on battery"
        else:
            charging_state = "Power state unknown"

        return f"Battery: {percent_str} | Status: {charging_state}"
    except Exception as error:
        return f"Could not retrieve battery status: {error}"


def open_notepad() -> str:
    """
    Opens the Windows Notepad text editor.
    """
    try:
        subprocess.Popen(["notepad.exe"])
        return "Opened Notepad."
    except Exception as error:
        return f"Could not open Notepad: {error}"


def open_calculator() -> str:
    """
    Opens the Windows Calculator.
    """
    try:
        os.startfile("calc:")
        return "Opened Calculator."
    except Exception:
        try:
            subprocess.Popen(["calc.exe"])
            return "Opened Calculator."
        except Exception as error:
            return f"Could not open Calculator: {error}"


def open_file_explorer() -> str:
    """
    Opens Windows File Explorer.
    """
    try:
        subprocess.Popen(["explorer.exe"])
        return "Opened File Explorer."
    except Exception as error:
        return f"Could not open File Explorer: {error}"


def open_settings() -> str:
    """
    Opens the Windows Settings application via the ms-settings protocol.
    """
    try:
        os.startfile("ms-settings:")
        return "Opened Windows Settings."
    except Exception as error:
        return f"Could not open Windows Settings: {error}"


def open_youtube() -> str:
    """
    Opens YouTube in the system's default web browser.
    """
    try:
        webbrowser.open("https://www.youtube.com")
        return "Opened YouTube in browser."
    except Exception as error:
        return f"Could not open YouTube: {error}"

