import requests
import feedparser

TOKEN = "8763023216:AAGTxJFJD2dnMtBHirSdx_fMhpyszuOkmS0"
CHAT_ID = "7330431242"

try:
    arabic = feedparser.parse(
        "https://news.google.com/rss?hl=ar&gl=SA&ceid=SA:ar"
    )

    english = feedparser.parse(
        "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en"
    )

    msg = "🔥 الترندات اليومية\n\n"

    msg += "🇸🇦 5 مواضيع عربية:\n"
    for i, item in enumerate(arabic.entries[:5], 1):
        msg += f"{i}- {item.title}\n"

    msg += "\n🌍 5 مواضيع إنجليزية:\n"
    for i, item in enumerate(english.entries[:5], 1):
        msg += f"{i}- {item.title}\n"

    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": msg
        }
    )

    print("Sent successfully")

except Exception as e:
    print(e)
