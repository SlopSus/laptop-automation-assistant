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
