import requests
import feedparser
import json
import os
import schedule
import time
import google.generativeai as genai

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

USED_FILE = "used_topics.json"
TOPICS_FILE = "topics.json"

last_article = ""
last_topic = ""
last_image_prompt = ""

def send_message(chat_id, text):
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={
            "chat_id": chat_id,
            "text": text[:4000]
        }
    )

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

def save_topics(data):
    with open(TOPICS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)

def load_topics():
    if os.path.exists(TOPICS_FILE):
        with open(TOPICS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

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

def generate_article(topic):

    prompt = f"""
اكتب مقال SEO احترافي باللغة العربية.

الموضوع:
{topic}

المطلوب:

- عنوان احترافي
- Meta Description
- مقدمة
- H2
- H3
- FAQ
- خاتمة
- 1200 إلى 1500 كلمة

وفي النهاية اكتب:

IMAGE_PROMPT:
وصف احترافي لصورة المقال.
"""

    response = model.generate_content(prompt)

    return response.text

def rewrite_article(article):

    prompt = f"""
أعد كتابة هذا المقال بشكل أفضل:

{article}
"""

    response = model.generate_content(prompt)

    return response.text

def modify_article(article, instruction):

    prompt = f"""
هذا المقال:

{article}

نفذ التعديل التالي:

{instruction}
"""

    response = model.generate_content(prompt)

    return response.text

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

    topics = {}

    message = "🔥 مواضيع اليوم للمقالات\n\n"

    message += "🇸🇦 5 مواضيع عربية\n\n"

    counter = 1

    for category, feeds in arabic_categories.items():

        topic = get_topic(feeds, used_topics)

        topics[str(counter)] = topic

        message += f"{counter}- {category}\n{topic}\n\n"

        counter += 1

    message += "🌍 5 مواضيع إنجليزية\n\n"

    for category, feeds in english_categories.items():

        topic = get_topic(feeds, used_topics)

        topics[str(counter)] = topic

        message += f"{counter}- {category}\n{topic}\n\n"

        counter += 1

    save_topics(topics)

    send_message(CHAT_ID, message)

    print("Topics Sent")

def get_updates(offset):

    response = requests.get(
        f"https://api.telegram.org/bot{TOKEN}/getUpdates",
        params={
            "offset": offset,
            "timeout": 20
        }
    )

    return response.json()

last_update_id = 0

schedule.every().day.at("05:00").do(send_daily_topics)

print("Bot Started")

while True:

    try:

        schedule.run_pending()

        updates = get_updates(last_update_id + 1)

        if updates.get("ok"):

            for update in updates["result"]:

                last_update_id = update["update_id"]

                if "message" not in update:
                    continue

                chat_id = str(update["message"]["chat"]["id"])

                text = update["message"].get("text", "").strip()

                topics = load_topics()

                global last_article
                global last_topic

                if text in topics:

                    selected_topic = topics[text]

                    last_topic = selected_topic

                    send_message(
                        chat_id,
                        f"✍️ جاري كتابة المقال:\n\n{selected_topic}"
                    )

                    article = generate_article(selected_topic)

                    last_article = article

                    send_message(chat_id, article)

                    send_message(
                        chat_id,
                        "✅ جاهز\n\nاكتب:\nانشر\nإعادة كتابة\nعدل: التعديل المطلوب\nعدل الصورة: الوصف الجديد"
                    )

                elif text == "إعادة كتابة":

                    if last_article:

                        article = rewrite_article(last_article)

                        last_article = article

                        send_message(chat_id, article)

                elif text.startswith("عدل:"):

                    if last_article:

                        instruction = text.replace("عدل:", "").strip()

                        article = modify_article(
                            last_article,
                            instruction
                        )

                        last_article = article

                        send_message(chat_id, article)

                elif text.startswith("عدل الصورة:"):

                    description = text.replace(
                        "عدل الصورة:",
                        ""
                    ).strip()

                    send_message(
                        chat_id,
                        f"🖼 وصف الصورة الجديد:\n\n{description}"
                    )

                elif text == "انشر":

                    send_message(
                        chat_id,
                        "🚀 النشر للموقع سنربطه بالمرحلة القادمة."
                    )

                elif text == "/start":

                    send_message(
                        chat_id,
                        "أرسل رقم الموضوع من 1 إلى 10 بعد وصول مواضيع اليوم."
                    )

    except Exception as e:

        print(e)

    time.sleep(3)
