"""
InfoVerse Hub V2
GitHub Publisher
"""

import base64
import requests

from config import (
    GITHUB_TOKEN,
    GITHUB_REPOSITORY,
    GITHUB_BRANCH,
)


class GitHubPublisher:

    def __init__(self):

        self.api = (
            f"https://api.github.com/repos/"
            f"{GITHUB_REPOSITORY}/contents"
        )

        self.headers = {
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Accept": "application/vnd.github+json",
        }
            def upload_file(
        self,
        content,
        path,
        message="Publish Article",
    ):
        """
        Upload file to GitHub.
        """

        url = f"{self.api}/{path}"

        encoded = base64.b64encode(
            content.encode("utf-8")
        ).decode("utf-8")

        data = {
            "message": message,
            "content": encoded,
            "branch": GITHUB_BRANCH,
        }

        response = requests.put(
            url,
            headers=self.headers,
            json=data,
            timeout=60,
        )

        if response.status_code not in (200, 201):

            raise Exception(
                response.text
            )

        return response.json()


    def publish_article(
        self,
        html,
        slug,
    ):
        """
        Publish article.
        """

        path = f"articles/{slug}/index.html"

        return self.upload_file(
            content=html,
            path=path,
            message=f"Publish {slug}",
        )
            def publish_image(
        self,
        image_path,
        slug,
        image_name,
    ):
        """
        Publish image.
        """

        with open(
            image_path,
            "rb"
        ) as file:

            encoded = base64.b64encode(
                file.read()
            ).decode("utf-8")

        path = f"articles/{slug}/images/{image_name}"

        data = {
            "message": f"Upload {image_name}",
            "content": encoded,
            "branch": GITHUB_BRANCH,
        }

        response = requests.put(
            f"{self.api}/{path}",
            headers=self.headers,
            json=data,
            timeout=60,
        )

        if response.status_code not in (200, 201):

            raise Exception(
                response.text
            )

        return response.json()


    def publish(
        self,
        html,
        slug,
        images=None,
    ):
        """
        Publish complete article.
        """

        self.publish_article(
            html,
            slug,
        )

        if images:

            for image in images:

                self.publish_image(
                    image_path=image["path"],
                    slug=slug,
                    image_name=image["path"].split("/")[-1],
                )

        print("✅ Article Published Successfully")


publisher = GitHubPublisher()
