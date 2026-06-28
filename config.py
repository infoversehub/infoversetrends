import os

# ==========================================
# TELEGRAM
# ==========================================

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# ==========================================
# GEMINI
# ==========================================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# ==========================================
# GITHUB
# ==========================================

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# ==========================================
# IMAGES API
# ==========================================

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
PIXABAY_API_KEY = os.getenv("PIXABAY_API_KEY")

# ==========================================
# JSON FILES
# ==========================================

TOPICS_FILE = "topics.json"
USED_TOPICS_FILE = "used_topics.json"
CURRENT_TOPIC_FILE = "current_topic.json"
CURRENT_ARTICLE_FILE = "current_article.json"
ARTICLE_VERSIONS_FILE = "article_versions.json"

# ==========================================
# DAILY SCHEDULE
# ==========================================

DAILY_SEND_TIME = "00:00"

# ==========================================
# PROJECT
# ==========================================

PROJECT_NAME = "InfoVerse Trends"
