import feedparser
import json
import re
from datetime import datetime, timezone

from config import (
    TOPICS_FILE,
    USED_TOPICS_FILE
)

from storage import (
    load_json,
    save_json
)


# ==========================================
# LOAD RSS SOURCES
# ==========================================

with open("rss_sources.json", "r", encoding="utf-8") as f:
    RSS_SOURCES = json.load(f)


# ==========================================
# LOAD USED TOPICS
# ==========================================

def load_used_topics():
    return load_json(USED_TOPICS_FILE, [])


def save_used_topics(data):
    save_json(USED_TOPICS_FILE, data[-300:])


# ==========================================
# LOAD TODAY TOPICS
# ==========================================

def load_topics():
    return load_json(TOPICS_FILE, {
        "date": "",
        "today": [],
        "history": []
    })


def save_topics(data):
    save_json(TOPICS_FILE, data)


# ==========================================
# TEXT HELPERS
# ==========================================

def clean_text(text):

    if not text:
        return ""

    text = re.sub(r"<[^>]+>", "", text)
    text = text.replace("\n", " ")
    text = text.replace("\r", " ")

    return " ".join(text.split())


def normalize_title(title):

    title = clean_text(title)

    return title.lower()
  # ==========================================
# FETCH NEWS
# ==========================================

def fetch_feed(feed_url):

    news = []

    try:
        feed = feedparser.parse(feed_url)

        for entry in feed.entries[:20]:

            title = clean_text(entry.get("title", ""))

            summary = clean_text(
                entry.get("summary", "")
                or entry.get("description", "")
            )

            link = entry.get("link", "")

            published = entry.get("published", "")

            if not title:
                continue

            news.append({
                "title": title,
                "summary": summary,
                "link": link,
                "published": published,
                "source": feed_url
            })

    except Exception as e:
        print(f"RSS Error: {feed_url} -> {e}")

    return news


# ==========================================
# SCORE
# ==========================================

GOOD_WORDS = [
    "new",
    "launch",
    "official",
    "update",
    "release",
    "ai",
    "gpt",
    "google",
    "apple",
    "microsoft",
    "tesla",
    "سامسونج",
    "جوجل",
    "آبل",
    "ذكاء",
    "رسمي",
    "إطلاق",
    "تحديث",
    "جديد"
]


def calculate_score(item):

    score = 0

    title = item["title"]
    summary = item["summary"]

    title_length = len(title)

    # مناسب للسيو
    if 40 <= title_length <= 90:
        score += 25

    # ملخص جيد
    if len(summary) >= 120:
        score += 20

    # يحتوي أرقام
    if any(c.isdigit() for c in title):
        score += 10

    # كلمات قوية
    for word in GOOD_WORDS:
        if word.lower() in title.lower():
            score += 10

    # وجود رابط
    if item["link"]:
        score += 5

    return score


# ==========================================
# FILTER
# ==========================================

def filter_news(news, used_topics):

    filtered = []

    seen = set()

    for item in news:

        title = normalize_title(item["title"])

        if title in seen:
            continue

        seen.add(title)

        if title in [normalize_title(x) for x in used_topics]:
            continue

        if len(item["title"]) < 25:
            continue

        item["score"] = calculate_score(item)

        filtered.append(item)

    filtered.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return filtered
  # ==========================================
# SELECT BEST NEWS
# ==========================================

def get_best_topic(category_name, feeds, used_topics):

    all_news = []

    for feed in feeds:

        news = fetch_feed(feed)

        all_news.extend(news)

    filtered = filter_news(all_news, used_topics)

    if len(filtered) == 0:

        return {
            "category": category_name,
            "title": "لم يتم العثور على موضوع مناسب",
            "summary": "",
            "link": "",
            "published": "",
            "source": "",
            "score": 0
        }

        best = filtered[0]

    candidates = []

    for item in filtered[:5]:
        candidates.append({
            "title": item["title"],
            "summary": item["summary"],
            "link": item["link"],
            "published": item["published"],
            "source": item["source"],
            "score": item["score"]
        })

    return {
        "category": category_name,
        "title": best["title"],
        "summary": best["summary"],
        "link": best["link"],
        "published": best["published"],
        "source": best["source"],
        "score": best["score"],
        "candidates": candidates
    }


# ==========================================
# BUILD TODAY TOPICS
# ==========================================

def build_today_topics():

    used_topics = load_used_topics()

    topics = []

    number = 1

    # Arabic
    for category, feeds in RSS_SOURCES["arabic"].items():

        topic = get_best_topic(
            category,
            feeds,
            used_topics
        )

        topic["number"] = number
        topic["language"] = "ar"

        topics.append(topic)

        used_topics.append(topic["title"])

        number += 1

    # English
    for category, feeds in RSS_SOURCES["english"].items():

        topic = get_best_topic(
            category,
            feeds,
            used_topics
        )

        topic["number"] = number
        topic["language"] = "en"

        topics.append(topic)

        used_topics.append(topic["title"])

        number += 1

    save_used_topics(used_topics)

    data = load_topics()

    data["today"] = topics

    data["history"].extend(topics)

    save_topics(data)

    return topics
  # ==========================================
# FORMAT TELEGRAM MESSAGE
# ==========================================

def build_telegram_message(topics):

    message = "🔥 مواضيع اليوم\n\n"

    message += "🇸🇦 المواضيع العربية\n\n"

    for topic in topics:

        if topic["language"] != "ar":
            continue

        message += (
            f'{topic["number"]}. {topic["category"]}\n'
            f'{topic["title"]}\n\n'
        )

    message += "🌍 المواضيع الإنجليزية\n\n"

    for topic in topics:

        if topic["language"] != "en":
            continue

        message += (
            f'{topic["number"]}. {topic["category"]}\n'
            f'{topic["title"]}\n\n'
        )

    return message.strip()


# ==========================================
# PUBLIC FUNCTION
# ==========================================

def generate_daily_topics():

    topics = build_today_topics()

    message = build_telegram_message(topics)

    return topics, message


# ==========================================
# FUTURE PROVIDERS
# ==========================================

"""
Future Sources

- RSS
- Google Trends
- Reddit
- Hacker News
- Product Hunt
- GitHub Trending
- X (Twitter) Trends

Each provider will return the same structure:

[
    {
        "title": "...",
        "summary": "...",
        "link": "...",
        "published": "...",
        "source": "...",
        "score": 95
    }
]

This allows adding new providers without changing
the selection logic.
"""
