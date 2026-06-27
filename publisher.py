from datetime import time

from telegram import Update
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from config import (
    BOT_TOKEN,
    CHAT_ID,
    CURRENT_TOPIC_FILE,
)

from storage import (
    load_json,
    save_json,
)

from topics import (
    generate_daily_topics,
)

# ==========================================
# CREATE APPLICATION
# ==========================================

application = (
    ApplicationBuilder()
    .token(BOT_TOKEN)
    .build()
)

# ==========================================
# GLOBAL CACHE
# ==========================================

TODAY_TOPICS = []
# ==========================================
# SEND DAILY TOPICS
# ==========================================

async def send_daily_topics(context: ContextTypes.DEFAULT_TYPE):

    global TODAY_TOPICS

    TODAY_TOPICS, message = generate_daily_topics()

    await context.bot.send_message(
        chat_id=CHAT_ID,
        text=message
    )

    print("✅ Daily topics sent.")


# ==========================================
# START COMMAND
# ==========================================

async def start_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        "🤖 InfoVerse Hub\n\n"
        "أرسل رقمًا من 1 إلى 11 لاختيار موضوع اليوم."
    )


# ==========================================
# STARTUP
# ==========================================

async def post_init(application: Application):

    # إرسال المواضيع عند أول تشغيل
    await application.bot.send_message(
        chat_id=CHAT_ID,
        text="🚀 Bot Started\n⏳ جاري جلب مواضيع اليوم..."
    )

    # تشغيل الجدولة اليومية
    application.job_queue.run_daily(
        send_daily_topics,
        time=time(hour=0, minute=0),
        name="daily_topics"
    )

    # إرسال المواضيع مباشرة لأول تشغيل
    await send_daily_topics(
        type(
            "StartupContext",
            (),
            {
                "bot": application.bot
            }
        )()
    )

    print("✅ JobQueue Started")
    # ==========================================
# RECEIVE USER MESSAGE
# ==========================================

async def receive_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if update.message is None:
        return

    text = update.message.text.strip()

    # اختيار موضوع
    if text.isdigit():

        number = int(text)

        if number < 1 or number > 11:

            await update.message.reply_text(
                "❌ اختر رقمًا من 1 إلى 11."
            )

            return

        data = load_json(
            "topics.json",
            {
                "today": []
            }
        )

        topics = data.get("today", [])

        selected = None

        for topic in topics:

            if topic["number"] == number:
                selected = topic
                break

        if selected is None:

            await update.message.reply_text(
                "❌ الموضوع غير موجود."
            )

            return

        save_json(
            CURRENT_TOPIC_FILE,
            selected
        )

        await update.message.reply_text(
            f"✅ تم اختيار:\n\n{selected['title']}\n\n"
            "⏳ جاري تحليل المصادر...\n"
            "⏳ جاري كتابة المقال..."
        )

        # المرحلة القادمة:
        # article = await gemini.generate_article(selected)

        return

    # أوامر المراحل القادمة

    if text.lower() == "انشر":

        await update.message.reply_text(
            "🚧 سيتم تفعيل النشر بعد ربط GitHub."
        )

        return

    if text.lower().startswith("عدل"):

        await update.message.reply_text(
            "🚧 سيتم تفعيل التعديل بعد ربط Gemini."
        )

        return

    if text.lower() == "ارجع للمقال الاول":

        await update.message.reply_text(
            "🚧 سيتم تفعيل الإصدارات بعد ربط Gemini."
        )

        return

    await update.message.reply_text(
        "❌ أرسل رقمًا من 1 إلى 11."
    )


# ==========================================
# HANDLERS
# ==========================================

application.add_handler(
    CommandHandler(
        "start",
        start_command
    )
)

application.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        receive_message
    )
)
# ==========================================
# MAIN
# ==========================================

def main():

    application.post_init = post_init

    print("=" * 50)
    print("InfoVerse Hub Started")
    print("=" * 50)

    application.run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True
    )


if __name__ == "__main__":
    main()
