"""
InfoVerse Hub V2
SEO Engine
"""

import re
from datetime import datetime

from config import SITE_NAME, SITE_URL


def create_slug(title):
    """
    Create SEO slug.
    """

    slug = title.lower()

    slug = re.sub(r"[^\w\s-]", "", slug)

    slug = re.sub(r"\s+", "-", slug)

    slug = re.sub(r"-+", "-", slug)

    return slug.strip("-")


def create_url(slug):
    """
    Build article URL.
    """

    return f"{SITE_URL}/{slug}/"


def create_canonical(url):
    """
    Canonical URL.
    """

    return url


def create_open_graph(title, description, url, image=""):
    """
    Open Graph tags.
    """

    return {
        "og:title": title,
        "og:description": description,
        "og:type": "article",
        "og:url": url,
        "og:image": image,
        "og:site_name": SITE_NAME,
    }


def create_twitter_card(title, description, image=""):
    """
    Twitter Card.
    """

    return {
        "twitter:card": "summary_large_image",
        "twitter:title": title,
        "twitter:description": description,
        "twitter:image": image,
    }


def create_schema(title, description, url, image=""):
    """
    Schema.org Article.
    """

    return {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "description": description,
        "url": url,
        "image": image,
        "datePublished": datetime.utcnow().isoformat(),
        "publisher": {
            "@type": "Organization",
            "name": SITE_NAME,
        },
    }


def build_seo(title, description):
    """
    Build complete SEO package.
    """

    slug = create_slug(title)

    url = create_url(slug)

    seo = {
        "slug": slug,
        "url": url,
        "canonical": create_canonical(url),
        "open_graph": create_open_graph(
            title,
            description,
            url,
        ),
        "twitter": create_twitter_card(
            title,
            description,
        ),
        "schema": create_schema(
            title,
            description,
            url,
        ),
    }

    return seo
