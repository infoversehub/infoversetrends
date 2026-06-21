import requests
import feedparser

TOKEN = "8763023216:AAGTxJFJD2dnMtBHirSdx_fMhpyszuOkmS0"
CHAT_ID = "7330431242"

feeds = {
    "🤖 الذكاء الاصطناعي": [
        "https://aitnews.com/feed/",
        "https://techcrunch.com/category/artificial-intelligence/feed/",
    ],

    "📱 التقنية والجوالات والسيارات": [
        "https://www.unlimit-tech.com/feed/",
        "https://www.theverge.com/rss/index.xml",
        "https://www.androidauthority.com/feed/",
    ],

    "💰 المال والاستثمار والذهب": [
        "https://www.investing.com/rss/news.rss",
        "https://www.kitco.com/rss/news",
        "https://feeds.feedburner.com/entrepreneur/latest",
    ],

    "✈️ السفر والهجرة والتأشيرات": [
        "https://www.travelandleisure.com/rss",
        "https://www.lonelyplanet.com/news/rss",
    ],

    "🎓 التعليم والمهارات": [
        "https://www.edutopia.org/rss.xml",
        "https://www.coursera.org/articles/rss",
    ],

    "🤖 AI": [
        "https://techcrunch.com/category/artificial-intelligence/feed/",
        "https://venturebeat.com/category/ai/feed/",
    ],

    "📱 Technology": [
        "https://www.theverge.com/rss/index.xml",
        "https://techcrunch.com/feed/",
    ],

    "💰 Finance": [
        "https://www.investing.com/rss/news.rss",
        "https://feeds.feedburner.com/entrepreneur/latest",
    ],

    "🎮 Gaming": [
        "https://www.ign.com/rss",
        "https://feeds.feedburner.com/Kotaku",
    ],

    "🚗 Automotive": [
        "https://www.motortrend.com/feed/",
        "https://www.autoblog.com/rss.xml",
    ]
}

message = "🔥 مواضيع اليوم للمقالات\n\n"

count = 1

for category, urls in feeds.items():

    title_found = None

    for url in urls:
        try:
            feed = feedparser.parse(url)

            if len(feed.entries) > 0:
                title_found = feed.entries[0].title
                break

        except:
            pass

    if title_found:
        message += f"{count}- {category}\n{title_found}\n\n"
        count += 1

requests.post(
    f"https://api.telegram.org/bot{TOKEN}/sendMessage",
    data={
        "chat_id": CHAT_ID,
        "text": message[:4000]
    }
)

print("Done")
