import os
import time
import requests
import google.generativeai as genai

TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

last_update_id = 0

topics = {}

last_article = ""
last_topic = ""

def send_message(chat_id, text):
    requests.post(
        f"{BASE_URL}/sendMessage",
        data={
            "chat_id": chat_id,
            "text": text[:4000]
        }
    )

def generate_article(topic):

    prompt = f"""
اكتب مقال احترافي SEO عربي.

الموضوع:
{topic}

المطلوب:

- عنوان جذاب
- مقدمة
- H2
- H3
- FAQ
- خاتمة
- 1200 كلمة تقريباً
- تنسيق مرتب
"""

    response = model.generate_content(prompt)

    return response.text

def get_updates():

    global last_update_id

    r = requests.get(
        f"{BASE_URL}/getUpdates",
        params={
            "offset": last_update_id + 1,
            "timeout": 30
        }
    )

    data = r.json()

    if not data["ok"]:
        return []

    updates = data["result"]

    if updates:
        last_update_id = updates[-1]["update_id"]

    return updates

print("Publisher Running...")

while True:

    try:

        updates = get_updates()

        for update in updates:

            if "message" not in update:
                continue

            chat_id = update["message"]["chat"]["id"]

            text = update["message"].get("text", "")

            if text.isdigit():

                topic_number = int(text)

                topic = topics.get(topic_number)

                if not topic:
                    send_message(chat_id, "ما لقيت الموضوع.")
                    continue

                send_message(chat_id, "⏳ جاري كتابة المقال...")

                article = generate_article(topic)

                last_article = article
                last_topic = topic

                send_message(chat_id, article)

            elif text == "إعادة كتابة":

                if not last_topic:
                    continue

                send_message(chat_id, "⏳ إعادة كتابة المقال...")

                article = generate_article(last_topic)

                last_article = article

                send_message(chat_id, article)

            elif text.startswith("عدل"):

                if not last_article:
                    continue

                instruction = text

                prompt = f"""
هذا المقال:

{last_article}

قم بتنفيذ التعديل التالي:

{instruction}
"""

                article = model.generate_content(prompt).text

                last_article = article

                send_message(chat_id, article)

            elif text == "انشر":

                send_message(
                    chat_id,
                    "✅ أمر النشر استُلم. سنربطه بالموقع لاحقاً."
                )

    except Exception as e:
        print(e)

    time.sleep(2)
