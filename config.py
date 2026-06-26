import os

# Telegram
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# JSON Files
TOPICS_FILE = "topics.json"
USED_TOPICS_FILE = "used_topics.json"
CURRENT_TOPIC_FILE = "current_topic.json"
CURRENT_ARTICLE_FILE = "current_article.json"
ARTICLE_VERSIONS_FILE = "article_versions.json"

# Daily Schedule
DAILY_SEND_TIME = "00:00"

# Project
PROJECT_NAME = "InfoVerse Trends"
