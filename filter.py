"""
InfoVerse Hub V2
Topics Filter
"""


def clean_text(text):
    """
    Clean text.
    """

    if not text:
        return ""

    return " ".join(text.split()).strip()


def remove_duplicates(articles):
    """
    Remove duplicate articles by title.
    """

    seen = set()
    unique = []

    for article in articles:

        title = clean_text(article.get("title", "")).lower()

        if not title:
            continue

        if title in seen:
            continue

        seen.add(title)

        article["title"] = clean_text(article["title"])
        article["summary"] = clean_text(article.get("summary", ""))

        unique.append(article)

    return unique


def remove_invalid_articles(articles):
    """
    Remove invalid articles.
    """

    filtered = []

    for article in articles:

        title = article.get("title", "")

        if len(title) < 15:
            continue

        if not article.get("link"):
            continue

        filtered.append(article)

    return filtered


def filter_articles(articles):
    """
    Run all filters.
    """

    articles = remove_duplicates(articles)

    articles = remove_invalid_articles(articles)

    return articles
