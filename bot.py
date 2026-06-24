import requests
import feedparser
import json
import os
import schedule
import time
TOKEN = "حط_التوكن_هنا"
CHAT_ID = "7330431242"
USED_FILE = "used_topics.json"
def load_used():
    if os.path.exists(USED_FILE):
        try:
            with open(USED_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []
def save_used(data):
    with open(USED_FILE, "w", encoding="utf-8") as f:
        json.dump(data[-100:], f, ensure_ascii=False)
def get_topic(sources, used_topics):
    for source in sources:
        try:
            feed = feedparser.parse(source)
            for entry in feed.entries:
                title = entry.title.strip()
                if title in used_topics:
                    continue
                used_topics.append(title)
                save_used(used_topics)
                return title
        except:
            pass
    return "لم يتم العثور على موضوع اليوم"
arabic_categories = {
    "🤖 الذكاء الاصطناعي": [
        "https://aitnews.com/feed/",
        "https://www.tech-wd.com/wd/feed/",
        "https://www.unlimit-tech.com/feed/",
        "https://www.arabapps.org/feed/",
        "https://www.ngmisr.com/feed/"
    ],
    "📱 التقنية والجوالات والسيارات": [
        "https://www.unlimit-tech.com/feed/",
        "https://www.tech-wd.com/wd/feed/",
        "https://www.androidauthority.com/feed/",
        "https://www.gsmarena.com/rss-news-reviews.php3",
        "https://www.motortrend.com/feed/"
    ],
    "💰 المال والاستثمار والذهب": [
        "https://www.investing.com/rss/news.rss",
        "https://www.kitco.com/rss/news",
        "https://finance.yahoo.com/rss/",
        "https://feeds.feedburner.com/entrepreneur/latest",
        "https://www.forbes.com/advisor/feed/"
    ],
    "✈️ السفر والهجرة والتأشيرات": [
        "https://www.travelandleisure.com/rss",
        "https://www.lonelyplanet.com/news/rss",
        "https://rss.nytimes.com/services/xml/rss/nyt/Travel.xml",
        "https://visaguide.world/feed/",
        "https://www.schengenvisainfo.com/feed/"
    ],
    "🎓 التعليم والمهارات": [
        "https://www.edutopia.org/rss.xml",
        "https://www.coursera.org/articles/rss",
        "https://www.edsurge.com/news.rss",
        "https://www.futurelearn.com/info/blog/feed",
        "https://blog.khanacademy.org/feed/"
    ]
}
english_categories = {
    "🤖 AI": [
        "https://techcrunch.com/category/artificial-intelligence/feed/",
        "https://venturebeat.com/category/ai/feed/",
        "https://www.marktechpost.com/feed/",
        "https://analyticsindiamag.com/feed/",
        "https://www.artificialintelligence-news.com/feed/"
    ],
    "📱 Technology": [
        "https://www.theverge.com/rss/index.xml",
        "https://techcrunch.com/feed/",
        "https://www.androidauthority.com/feed/",
        "https://www.gsmarena.com/rss-news-reviews.php3",
        "https://arstechnica.com/feed/"
    ],
    "💰 Finance": [
        "https://finance.yahoo.com/rss/",
        "https://www.investing.com/rss/news.rss",
        "https://www.marketwatch.com/rss/topstories",
        "https://feeds.feedburner.com/entrepreneur/latest",
        "https://www.forbes.com/advisor/feed/"
    ],
    "🎮 Gaming": [
        "https://www.ign.com/rss",
        "https://feeds.feedburner.com/Kotaku",
        "https://www.gamespot.com/feeds/mashup/",
        "https://www.pcgamer.com/rss/",
        "https://www.eurogamer.net/feed"
    ],
    "🚗 Automotive": [
        "https://www.motortrend.com/feed/",
        "https://www.autoblog.com/rss.xml",
        "https://www.caranddriver.com/rss/all.xml/",
        "https://insideevs.com/rss/news/",
        "https://www.topgear.com/rss.xml"
    ]
}
def send_daily_topics():
    used_topics = load_used()
    message = "🔥 مواضيع اليوم للمقالات\n\n"
    message += "🇸🇦 5 مواضيع عربية\n\n"
    counter = 1
    for category, feeds in arabic_categories.items():
        topic = get_topic(feeds, used_topics)
        message += f"{counter}- {category}\n{topic}\n\n"
        counter += 1
    message += "🌍 5 مواضيع إنجليزية\n\n"
    counter = 1
    for category, feeds in english_categories.items():
        topic = get_topic(feeds, used_topics)
        message += f"{counter}- {category}\n{topic}\n\n"
        counter += 1
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": message[:4000]
        }
    )
    print("Topics Sent")
schedule.every().day.at("02:00").do(send_daily_topics)
while True:
    schedule.run_pending()
    time.sleep(60)
