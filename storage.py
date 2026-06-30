"""
InfoVerse Hub V2
Storage Manager
"""

import json
import os


def load_json(filename, default=None):
    """
    Load JSON file.
    """

    if default is None:
        default = {}

    if not os.path.exists(filename):
        return default

    try:

        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)

    except Exception:

        return default


def save_json(filename, data):
    """
    Save JSON file.
    """

    with open(filename, "w", encoding="utf-8") as file:

        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=4
        )


def file_exists(filename):
    """
    Check if file exists.
    """

    return os.path.exists(filename)


def delete_file(filename):
    """
    Delete file.
    """

    if os.path.exists(filename):
        os.remove(filename)
