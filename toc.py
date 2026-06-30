"""
InfoVerse Hub V2
Table of Contents Builder
"""

from bs4 import BeautifulSoup


class TOCBuilder:

    def __init__(self):

        pass


    def build(self, html):
        """
        Build TOC from H2 headings.
        """

        soup = BeautifulSoup(
            html,
            "html.parser"
        )

        headings = soup.find_all("h2")

        toc = []

        for index, heading in enumerate(headings, start=1):

            title = heading.get_text(strip=True)

            anchor = f"section-{index}"

            heading["id"] = anchor

            toc.append({
                "title": title,
                "anchor": anchor,
            })

        return str(soup), toc


toc_builder = TOCBuilder()
    def render(self, toc):
        """
        Render HTML TOC.
        """

        if not toc:
            return ""

        html = [
            '<ul class="toc-list">'
        ]

        for item in toc:

            html.append(
                f'''
<li>
<a href="#{item["anchor"]}">
{item["title"]}
</a>
</li>
'''
            )

        html.append("</ul>")

        return "\n".join(html)


    def generate(self, article_html):
        """
        Generate complete TOC.
        """

        article_html, toc = self.build(
            article_html
        )

        toc_html = self.render(
            toc
        )

        return {
            "content": article_html,
            "toc": toc_html,
            "items": toc,
        }


toc_builder = TOCBuilder()
