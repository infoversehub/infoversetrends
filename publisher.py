"""
InfoVerse Hub V2
Publisher
"""

from parser import parse_article

from seo import build_seo

from images import image_engine

from template import builder

from preview import preview

from github_publish import publisher


class Publisher:

    def __init__(self):

        pass
            def publish(
        self,
        article_html,
    ):
        """
        Publish article workflow.
        """

        print("Parsing article...")

        article = parse_article(
            article_html
        )

        print("Building SEO...")

        seo = build_seo(
            article
        )

        print("Searching images...")

        images = image_engine.get_images(
            article
        )

        print("Building page...")

        html = builder.build(
            article=article,
            seo=seo,
            images=images,
        )

        print("Generating preview...")

        preview.save(
            html
        )

        return {
            "article": article,
            "seo": seo,
            "images": images,
            "html": html,
        }
            def publish_to_github(
        self,
        article_html,
    ):
        """
        Publish article to GitHub.
        """

        result = self.publish(
            article_html
        )

        publisher.publish(
            html=result["html"],
            slug=result["seo"]["slug"],
            images=result["images"]["images"],
        )

        print("Done.")

        return result


publisher_engine = Publisher()
