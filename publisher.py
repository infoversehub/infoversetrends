import os
import json
import requests
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

TOPICS_FILE = "topics.json"


def load_topics():
    try:
        with open(TOPICS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"today": []}


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if not text.isdigit():
        return

    number = int(text)

    topics = load_topics()

    selected = None

    for topic in topics.get("today", []):
        if topic["number"] == number:
            selected = topic
            break

    if not selected:
        await update.message.reply_text(
            "❌ الرقم غير موجود ضمن مواضيع اليوم"
        )
        return

    await update.message.reply_text(
        f"✅ تم اختيار الموضوع\n\n"
        f"{selected['category']}\n\n"
        f"{selected['title']}"
    )


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    print("Publisher Started")

    app.run_polling()


if __name__ == "__main__":
    main()
