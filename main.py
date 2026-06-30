"""
InfoVerse Hub V2
Main Controller
"""

from bot import start_bot
from topics import collect_topics


def main():

    print("=" * 50)
    print("InfoVerse Hub V2")
    print("=" * 50)

    collect_topics()

    start_bot()


if __name__ == "__main__":
    main()
