"""
main.py
-------
The main entry point for Laptop Automation Assistant.
Runs the interactive Command-Line Interface (CLI) loop.
"""

from commands import process_command


def print_banner() -> None:
    """Prints a welcoming header when the program starts."""
    banner = (
        "\n"
        "=====================================================\n"
        "       Laptop Automation Assistant (v1.2)           \n"
        "=====================================================\n"
        " - Type any text command (e.g. 'open chrome')\n"
        " - Type 'voice' or 'listen' to speak into microphone\n"
        " - Type 'help' to see all commands\n"
        " - Type 'exit' to quit\n"
    )
    print(banner)


def main() -> None:
    """Runs the main interactive loop for the assistant."""
    print_banner()

    while True:
        try:
            # Prompt the user for input
            user_input = input("Assistant > ")

            # Send input to command processor
            response, keep_running = process_command(user_input)

            # Display the result
            print(response)
            print()  # Add a clean blank line between interactions

            # Check if the user requested to exit
            if not keep_running:
                break

        except (KeyboardInterrupt, EOFError):
            # Gracefully handle Ctrl+C or Ctrl+Z without showing an ugly traceback
            print("\n\nSession ended. Goodbye!")
            break


if __name__ == "__main__":
    main()
