from datetime import time

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
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

from gemini import (
    create_article,
)

from github import (
    publish_article,
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

LAST_ARTICLE = None

# ==========================================
# SEND DAILY TOPICS
# ==========================================

async def send_daily_topics(
    context: ContextTypes.DEFAULT_TYPE
):

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
        "أرسل رقم الموضوع لبدء كتابة المقال."
    )

# ==========================================
# STARTUP
# ==========================================

async def post_init(
    application: Application
):

    await application.bot.send_message(
        chat_id=CHAT_ID,
        text="🚀 Bot Started\n⏳ جاري جلب مواضيع اليوم..."
    )

    application.job_queue.run_daily(
        send_daily_topics,
        time=time(
            hour=0,
            minute=0
        ),
        name="daily_topics"
    )

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

    global LAST_ARTICLE

    if update.message is None:
        return

    text = update.message.text.strip()

    # ==========================================
    # SELECT TOPIC
    # ==========================================

    if text.isdigit():

        number = int(text)

        data = load_json(
            "topics.json",
            {
                "today": []
            }
        )

        topics = data.get(
            "today",
            []
        )

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
            "⏳ جاري كتابة المقال...\n"
            "قد يستغرق ذلك دقيقة أو دقيقتين."
        )

        result = create_article(selected)

        if not result["success"]:

            await update.message.reply_text(
                "❌ فشل إنشاء المقال."
            )

            return

        article = result["data"]

        LAST_ARTICLE = article

        await update.message.reply_text(
            f"✅ تم إنشاء المقال.\n\n"
            f"📌 {article['title']}\n\n"
            f"📝 {article['meta_description']}"
        )

        article_text = article["article"]

        MAX_LENGTH = 3500

        for i in range(
            0,
            len(article_text),
            MAX_LENGTH
        ):

            part = article_text[
                i:i + MAX_LENGTH
            ]

            await update.message.reply_text(
                part
            )

        await update.message.reply_text(
            "━━━━━━━━━━━━━━━━━━\n\n"
            "✅ انتهى إرسال المقال.\n\n"
            "اكتب:\n"
            "📤 انشر\n"
            "✏️ عدل"
        )

        return
# ==========================================
# PUBLISH / EDIT COMMANDS
# ==========================================

    if text.lower() == "انشر":

        if LAST_ARTICLE is None:

            await update.message.reply_text(
                "❌ لا يوجد مقال للنشر."
            )

            return

        await update.message.reply_text(
            "🚀 جاري النشر على GitHub..."
        )

        success = publish_article(
            LAST_ARTICLE
        )

        if success:

            slug = LAST_ARTICLE["slug"]

            await update.message.reply_text(
                "✅ تم نشر المقال بنجاح.\n\n"
                f"📄 articles/{slug}.html"
            )

        else:

            await update.message.reply_text(
                "❌ فشل النشر على GitHub."
            )

        return

    # ==========================================

    if text.lower() == "عدل":

        if LAST_ARTICLE is None:

            await update.message.reply_text(
                "❌ لا يوجد مقال لتعديله."
            )

            return

        await update.message.reply_text(
            "✏️ ميزة التعديل سيتم إضافتها قريبًا."
        )

        return

    # ==========================================

    await update.message.reply_text(
        "❌ أرسل رقم موضوع أو اكتب (انشر)."
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
