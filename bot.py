import requests
import feedparser

TOKEN = "8763023216:AAGTxJFJD2dnMtBHirSdx_fMhpyszuOkmS0"
CHAT_ID = "7330431242"

arabic_sources = [
    "https://news.google.com/rss?hl=ar&gl=SA&ceid=SA:ar",
    "https://arabic.cnn.com/rss",
]

english_sources = [
    "https://news.google.com/rss/search?q=Artificial+Intelligence&hl=en-US&gl=US&ceid=US:en",
    "https://news.google.com/rss/search?q=Technology&hl=en-US&gl=US&ceid=US:en",
    "https://news.google.com/rss/search?q=Cars&hl=en-US&gl=US&ceid=US:en",
    "https://news.google.com/rss/search?q=Business&hl=en-US&gl=US&ceid=US:en",
    "https://news.google.com/rss/search?q=Gaming&hl=en-US&gl=US&ceid=US:en",
    "https://news.google.com/rss/search?q=Sports&hl=en-US&gl=US&ceid=US:en",
    "https://news.google.com/rss/search?q=Smartphones&hl=en-US&gl=US&ceid=US:en",
    "https://news.google.com/rss/search?q=World&hl=en-US&gl=US&ceid=US:en",
]

used_words = set()

def is_duplicate(title):
    words = set(
        w.lower()
        for w in title.split()
        if len(w) > 4
    )

    overlap = len(words & used_words)

    if overlap >= 2:
        return True

    used_words.update(words)
    return False


arabic_topics = []
english_topics = []

for source in arabic_sources:
    try:
        feed = feedparser.parse(source)

        for item in feed.entries:
            title = item.title.split(" - ")[0]

            if not is_duplicate(title):
                arabic_topics.append(title)

            if len(arabic_topics) >= 5:
                break

        if len(arabic_topics) >= 5:
            break

    except:
        pass


for source in english_sources:
    try:
        feed = feedparser.parse(source)

        for item in feed.entries:
            title = item.title.split(" - ")[0]

            if not is_duplicate(title):
                english_topics.append(title)

            if len(english_topics) >= 5:
                break

        if len(english_topics) >= 5:
            break

    except:
        pass


message = "🔥 مواضيع اليوم للمقالات\n\n"

message += "🇸🇦 5 مواضيع عربية\n\n"

for i, topic in enumerate(arabic_topics[:5], 1):
    message += f"{i}- {topic}\n"

message += "\n🌍 5 مواضيع إنجليزية\n\n"

for i, topic in enumerate(english_topics[:5], 1):
    message += f"{i}- {topic}\n"

requests.post(
    f"https://api.telegram.org/bot{TOKEN}/sendMessage",
    data={
        "chat_id": CHAT_ID,
        "text": message[:4000]
    }
)

print("Done")
