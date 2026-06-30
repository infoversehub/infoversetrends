"""
InfoVerse Hub V2
Template Builder
"""

import os


class TemplateBuilder:

    def __init__(self):

        self.template_path = "template.html"

    def load_template(self):
        """
        Load HTML template.
        """

        with open(
            self.template_path,
            "r",
            encoding="utf-8"
        ) as file:

            return file.read()


    def replace(self, html, key, value):
        """
        Replace placeholder.
        """

        if value is None:
            value = ""

        return html.replace(
            "{{" + key + "}}",
            str(value)
        )
          def fill_template(
        self,
        article,
        seo,
        images,
        related_articles="",
        toc="",
        faq="",
        comparison="",
        buying_tips="",
    ):
        """
        Fill HTML template.
        """

        html = self.load_template()

        html = self.replace(
            html,
            "TITLE",
            article.get("title", "")
        )

        html = self.replace(
            html,
            "DATE",
            article.get("date", "")
        )

        html = self.replace(
            html,
            "DESCRIPTION",
            article.get("meta_description", "")
        )

        html = self.replace(
            html,
            "SUMMARY",
            article.get("summary", "")
        )

        html = self.replace(
            html,
            "CONTENT",
            article.get("html", "")
        )

        html = self.replace(
            html,
            "FEATURED_IMAGE",
            images["featured"]["path"]
            if images.get("featured")
            else ""
        )

        html = self.replace(
            html,
            "TOC",
            toc
        )

        html = self.replace(
            html,
            "FAQ",
            faq
        )

        html = self.replace(
            html,
            "COMPARISON",
            comparison
        )

        html = self.replace(
            html,
            "BUYING_TIPS",
            buying_tips
        )

        html = self.replace(
            html,
            "RELATED_ARTICLES",
            related_articles
        )

        return html
          def build(
        self,
        article,
        seo,
        images,
        related_articles="",
        toc="",
        faq="",
        comparison="",
        buying_tips="",
    ):
        """
        Build final HTML page.
        """

        html = self.fill_template(
            article=article,
            seo=seo,
            images=images,
            related_articles=related_articles,
            toc=toc,
            faq=faq,
            comparison=comparison,
            buying_tips=buying_tips,
        )

        # SEO
        html = self.replace(
            html,
            "SLUG",
            seo.get("slug", "")
        )

        html = self.replace(
            html,
            "URL",
            seo.get("url", "")
        )

        html = self.replace(
            html,
            "CANONICAL",
            seo.get("canonical", "")
        )

        html = self.replace(
            html,
            "SCHEMA",
            seo.get("schema", "")
        )

        html = self.replace(
            html,
            "OPEN_GRAPH",
            seo.get("open_graph", "")
        )

        html = self.replace(
            html,
            "TWITTER_CARD",
            seo.get("twitter", "")
        )

        return html


builder = TemplateBuilder()
