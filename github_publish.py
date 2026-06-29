from datetime import datetime

from github import (
    upload_file,
)

# ==========================================
# LOAD TEMPLATE
# ==========================================

def load_template():

    with open(
        "template.html",
        "r",
        encoding="utf-8"
    ) as file:

        return file.read()

# ==========================================
# BUILD HTML
# ==========================================

def build_html(article):

    html = load_template()

    html = html.replace(
        "{{TITLE}}",
        article["title"]
    )

    html = html.replace(
        "{{DESCRIPTION}}",
        article["meta_description"]
    )

    html = html.replace(
        "{{CONTENT}}",
        article["article"]
    )

    html = html.replace(
        "{{CATEGORY}}",
        article.get(
            "category",
            "General"
        )
    )

    html = html.replace(
        "{{DATE}}",
        datetime.now().strftime(
            "%Y-%m-%d"
        )
    )

    html = html.replace(
        "{{YEAR}}",
        str(
            datetime.now().year
        )
    )

    html = html.replace(
        "{{AUTHOR}}",
        "InfoVerse Hub"
    )

    html = html.replace(
        "{{LANG}}",
        "ar"
    )

    html = html.replace(
        "{{DIR}}",
        "rtl"
    )

    html = html.replace(
        "{{LANGUAGE}}",
        "Arabic"
    )
    
    hero_image = "https://placehold.co/1200x630?text=InfoVerse+Hub"

    if article.get("images"):
        hero_image = article["images"][0]["url"]

   html = html.replace(
        "{{IMAGE}}",
        hero_image
  )

    html = html.replace(
        "{{KEYWORDS}}",
        ", ".join(
            article.get(
                "keywords",
                []
            )
        )
    )

    html = html.replace(
        "{{CANONICAL_URL}}",
        article.get(
            "url",
            "#"
        )
    )

    html = html.replace(
        "{{READING_TIME}}",
        article.get(
            "reading_time",
            "5 min"
        )
    )

    html = html.replace(
        "{{TOC}}",
        article.get(
            "toc",
            ""
        )
    )

    html = html.replace(
        "{{FAQ}}",
        article.get(
            "faq",
            ""
        )
    )

    html = html.replace(
        "{{RELATED_ARTICLES}}",
        article.get(
            "related_articles",
            ""
        )
    )

    images_html = ""

    for image in article.get("images", []):
        images_html += f"""
    <figure class="article-image">
        <img src="{image['url']}"
             alt="{image.get('alt', article['title'])}"
             loading="lazy">
    </figure>
    """

    html = html.replace(
        "{{IMAGES}}",
        images_html
   )
    
    return html

# ==========================================
# PUBLISH ARTICLE
# ==========================================

def publish_article(article):

    slug = article["slug"]

    html = build_html(
        article
    )
    success = upload_file(
        path=f"articles/{slug}.html",
        content=html,
        message=f"Publish article: {article['title']}"
      )
    return success

# ==========================================
# PUBLISH PREVIEW
# ==========================================

def publish_preview(article):

    html = build_html(
        article
    )

    success = upload_file(
        path="preview/index.html",
        content=html,
        message="Update Preview"
    )

    if not success:

        return None

    return (
        "https://infoversehub.github.io/"
"infoversetrends/preview/"
    )
