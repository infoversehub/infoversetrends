"""
InfoVerse Hub V2
History Manager
"""

import json
import os


HISTORY_FILE = "used_topics.json"


class HistoryManager:

    def __init__(self):

        pass


    def load(self):

        if not os.path.exists(HISTORY_FILE):

            return []

        with open(
            HISTORY_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)


    def save(
        self,
        history,
    ):

        with open(
            HISTORY_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                history,
                file,
                ensure_ascii=False,
                indent=4,
            )


    def exists(
        self,
        title,
    ):

        history = self.load()

        return title.lower() in [
            item.lower()
            for item in history
        ]


    def add(
        self,
        title,
    ):

        history = self.load()

        if title not in history:

            history.append(title)

        history = history[-300:]

        self.save(history)


history_manager = HistoryManager()
