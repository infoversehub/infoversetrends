import requests
import feedparser

TOKEN = "8763023216:AAGTxJFJD2dnMtBHirSdx_fMhpyszuOkmS0"
CHAT_ID = "7330431242"

feeds = {
    "🤖 AI": "https://news.google.com/rss/search?q=AI&hl=en-US&gl=US&ceid=US:en",
    "📱 Tech": "https://news.google.com/rss/search?q=Technology&hl=en-US&gl=US&ceid=US:en",
    "🚗 Cars": "https://news.google.com/rss/search?q=Cars&hl=en-US&gl=US&ceid=US:en",
    "🎮 Gaming": "https://news.google.com/rss/search?q=Gaming&hl=en-US&gl=US&ceid=US:en",
    "💰 Business": "https://news.google.com/rss/search?q=Business&hl=en-US&gl=US&ceid=US:en",
    "⚽ Sports": "https://news.google.com/rss/search?q=Sports&hl=en-US&gl=US&ceid=US:en",
    "🎬 Entertainment": "https://news.google.com/rss/search?q=Entertainment&hl=en-US&gl=US&ceid=US:en",
    "🌍 World": "https://news.google.com/rss/search?q=World&hl=en-US&gl=US&ceid=US:en",
    "🇸🇦 Arab": "https://news.google.com/rss?hl=ar&gl=SA&ceid=SA:ar",
    "🚀 Trending": "https://news.google.com/rss/search?q=Trending&hl=en-US&gl=US&ceid=US:en"
}

message = "🔥 مواضيع اليوم للمقالات\n\n"

count = 1

for category, url in feeds.items():
    try:
        feed = feedparser.parse(url)

        if len(feed.entries) > 0:
            title = feed.entries[0].title.split(" - ")[0]
            message += f"{count}- {category}\n{title}\n\n"
            count += 1

    except:
        pass

requests.post(
    f"https://api.telegram.org/bot{TOKEN}/sendMessage",
    data={
        "chat_id": CHAT_ID,
        "text": message[:4000]
    }
)

print("Done")
