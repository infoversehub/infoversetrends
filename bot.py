import requests
import feedparser

TOKEN = "8763023216:AAGTxJFJD2dnMtBHirSdx_fMhpyszuOkmS0"
CHAT_ID = "7330431242"

feeds_ar = [
    "https://www.tech-wd.com/wd/feed/",
    "https://aitnews.com/feed/",
    "https://www.arageek.com/feed"
]

feeds_en = [
    "https://techcrunch.com/feed/",
    "https://www.theverge.com/rss/index.xml",
    "https://feeds.feedburner.com/venturebeat/SZYF",
    "https://www.ign.com/rss",
    "https://www.businessinsider.com/rss"
]

message = "🔥 مواضيع اليوم للمقالات\n\n"

# عربي
message += "🇸🇦 5 مواضيع عربية:\n\n"

arab_topics = []
for feed_url in feeds_ar:
    try:
        feed = feedparser.parse(feed_url)
        for item in feed.entries[:5]:
            title = item.title.strip()
            if title not in arab_topics:
                arab_topics.append(title)
    except:
        pass

for i, topic in enumerate(arab_topics[:5], 1):
    message += f"{i}- {topic}\n"

message += "\n🌍 5 مواضيع إنجليزية:\n\n"

eng_topics = []
for feed_url in feeds_en:
    try:
        feed = feedparser.parse(feed_url)
        for item in feed.entries[:10]:
            title = item.title.strip()
            if title not in eng_topics:
                eng_topics.append(title)
    except:
        pass

for i, topic in enumerate(eng_topics[:5], 1):
    message += f"{i}- {topic}\n"

requests.post(
    f"https://api.telegram.org/bot{TOKEN}/sendMessage",
    data={
        "chat_id": CHAT_ID,
        "text": message[:4000]
    }
)

print("Done")
