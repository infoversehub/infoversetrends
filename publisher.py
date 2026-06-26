import asyncio
import threading
import schedule
import time

from telegram import Bot, Update
from telegram.ext import (
    Application,
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    filters,
)

from config import (
    BOT_TOKEN,
    CHAT_ID,
    CURRENT_TOPIC_FILE,
    DAILY_SEND_TIME,
)

from storage import (
    load_json,
    save_json,
)

from topics import (
    generate_daily_topics,
)


# ==========================================
# TELEGRAM BOT
# ==========================================

bot = Bot(token=BOT_TOKEN)

application = (
    ApplicationBuilder()
    .token(BOT_TOKEN)
    .build()
)
# ==========================================
# SEND DAILY TOPICS
# ==========================================

async def send_daily_topics():

    topics, message = generate_daily_topics()

    await bot.send_message(
        chat_id=CHAT_ID,
        text=message
    )

    print("✅ Daily topics sent.")

    return topics


# ==========================================
# STARTUP
# ==========================================

async def send_startup_topics():

    try:
        await send_daily_topics()
    except Exception as e:
        print(f"Startup Error: {e}")


# ==========================================
# SCHEDULER
# ==========================================

def scheduler_loop():

    schedule.every().day.at(DAILY_SEND_TIME).do(
        lambda: asyncio.run(send_daily_topics())
    )

    while True:
        schedule.run_pending()
        time.sleep(30)


def start_scheduler():

    thread = threading.Thread(
        target=scheduler_loop,
        daemon=True
    )

    thread.start()
    # ==========================================
# RECEIVE USER MESSAGES
# ==========================================

async def receive_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if update.message is None:
        return

    text = update.message.text.strip()

    # المرحلة الحالية: اختيار الموضوع
    if text.isdigit():

        number = int(text)

        if number < 1 or number > 11:

            await update.message.reply_text(
                "❌ أرسل رقمًا من 1 إلى 11."
            )

            return

        data = load_json(
            "topics.json",
            {
                "today": []
            }
        )

        topics = data.get("today", [])

        selected_topic = None

        for topic in topics:

            if topic["number"] == number:
                selected_topic = topic
                break

        if selected_topic is None:

            await update.message.reply_text(
                "❌ لم يتم العثور على الموضوع."
            )

            return

        save_json(
            CURRENT_TOPIC_FILE,
            selected_topic
        )

        await update.message.reply_text(
            "✅ تم اختيار الموضوع.\n\n"
            "⏳ جاري تحليل المصادر...\n"
            "⏳ جاري كتابة المقال..."
        )

        # المرحلة القادمة:
        # article = await generate_article(selected_topic)

        return

    # أوامر مستقبلية
    await update.message.reply_text(
        "❌ أمر غير معروف."
    )


# ==========================================
# HANDLERS
# ==========================================

application.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        receive_message
    )
)
# ==========================================
# MAIN
# ==========================================

async def on_startup():

    print("=" * 50)
    print("InfoVerse Trends Started")
    print("=" * 50)

    # إرسال المواضيع عند أول تشغيل (للاختبار)
    await send_startup_topics()

    # تشغيل الجدولة اليومية
    start_scheduler()

    print(f"✅ Daily Scheduler: {DAILY_SEND_TIME}")
    print("✅ Telegram Bot Ready")


def main():

    application.post_init = on_startup

    application.run_polling(
        drop_pending_updates=True,
        allowed_updates=Update.ALL_TYPES
    )


if __name__ == "__main__":
    main()
