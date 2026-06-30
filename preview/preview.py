"""
InfoVerse Hub V2
Preview Generator
"""

import os
import webbrowser

PREVIEW_FOLDER = "preview"

PREVIEW_FILE = "preview/index.html"


class PreviewBuilder:

    def __init__(self):

        os.makedirs(
            PREVIEW_FOLDER,
            exist_ok=True,
        )


    def save(self, html):
        """
        Save preview page.
        """

        with open(
            PREVIEW_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(html)

        return PREVIEW_FILE


    def open(self):
        """
        Open preview.
        """

        path = os.path.abspath(
            PREVIEW_FILE
        )

        webbrowser.open(
            f"file://{path}"
        )


preview = PreviewBuilder()
    def get_preview_url(self):
        """
        Return preview file path.
        """

        return os.path.abspath(
            PREVIEW_FILE
        )


    def exists(self):
        """
        Check preview exists.
        """

        return os.path.exists(
            PREVIEW_FILE
        )


    def delete(self):
        """
        Delete preview.
        """

        if self.exists():

            os.remove(
                PREVIEW_FILE
            )


    def rebuild(self, html):
        """
        Rebuild preview.
        """

        self.delete()

        self.save(
            html
        )

        return self.get_preview_url()


preview = PreviewBuilder()
