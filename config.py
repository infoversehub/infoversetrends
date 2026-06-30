"""
InfoVerse Hub V2
Configuration
"""

import os

# ==========================
# Telegram
# ==========================

BOT_TOKEN = os.getenv("BOT_TOKEN", "")

# ==========================
# Files
# ==========================

RSS_FILE = "rss_sources.json"

TOPICS_FILE = "topics.json"

HISTORY_FILE = "history.json"

PUBLISHED_FILE = "published.json"

# ==========================
# Topics
# ==========================

MAX_TOPICS = 10

MAX_ARTICLES_PER_FEED = 20

# ==========================
# Images
# ==========================

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY", "")

PIXABAY_API_KEY = os.getenv("PIXABAY_API_KEY", "")

# ==========================
# GitHub
# ==========================

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")

GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY", "")

GITHUB_BRANCH = "main"

# ==========================
# Preview
# ==========================

PREVIEW_FOLDER = "preview"

# ==========================
# Website
# ==========================

SITE_NAME = "InfoVerse Hub"

SITE_URL = "https://example.com"
