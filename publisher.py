"""
InfoVerse Hub V2
Main Controller

This file is the entry point of the entire system.
"""

from topics import collect_topics
from bot import start_bot


def main():
    print("=" * 50)
    print("InfoVerse Hub V2")
    print("Starting...")
    print("=" * 50)

    # Collect today's topics
    collect_topics()

    # Start Telegram bot
    start_bot()


if __name__ == "__main__":
    main()
