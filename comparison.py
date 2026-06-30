"""
InfoVerse Hub V2
Comparison Table Builder
"""

from bs4 import BeautifulSoup


class ComparisonBuilder:

    def __init__(self):

        self.keywords = [
            "vs",
            "VS",
            "مقارنة",
            "أفضل",
            "مقابل",
            "أم",
            "او",
            "أو",
        ]


    def needs_comparison(
        self,
        article,
    ):
        """
        Check if article needs comparison table.
        """

        title = article.get(
            "title",
            ""
        )

        for keyword in self.keywords:

            if keyword.lower() in title.lower():

                return True

        return False


    def build(
        self,
        article,
    ):
        """
        Build comparison table.
        """

        if not self.needs_comparison(article):

            return ""

        return """
<section class="comparison">

<h2>

جدول المقارنة

</h2>

<table>

<thead>

<tr>

<th>الميزة</th>

<th>الخيار الأول</th>

<th>الخيار الثاني</th>

</tr>

</thead>

<tbody>

{{COMPARISON_ROWS}}

</tbody>

</table>

</section>
"""


comparison_builder = ComparisonBuilder()
    def build_rows(
        self,
        items,
    ):
        """
        Build comparison rows.
        """

        rows = []

        for item in items:

            rows.append(f"""
<tr>

<td>{item.get("feature","")}</td>

<td>{item.get("first","")}</td>

<td>{item.get("second","")}</td>

</tr>
""")

        return "\n".join(rows)


    def render(
        self,
        article,
        items,
    ):
        """
        Render comparison section.
        """

        html = self.build(article)

        if not html:
            return ""

        rows = self.build_rows(
            items
        )

        return html.replace(
            "{{COMPARISON_ROWS}}",
            rows,
        )


comparison_builder = ComparisonBuilder()
