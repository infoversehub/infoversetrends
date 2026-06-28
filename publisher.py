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
    CallbackQueryHandler,
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
# GLOBALS
# ==========================================

TODAY_TOPICS = []

LAST_ARTICLE = None

# ==========================================
# DAILY TOPICS
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
        "أرسل رقم الموضوع."
    )

# ==========================================
# STARTUP
# ==========================================

async def post_init(
    application: Application
):

    await application.bot.send_message(
        chat_id=CHAT_ID,
        text="🚀 Bot Started\n\n⏳ جاري جلب مواضيع اليوم..."
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
# RECEIVE MESSAGE
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

        if selected["title"] == "لا يوجد موضوع مناسب اليوم":

            await update.message.reply_text(
                "❌ لا يوجد موضوع لهذا الرقم."
            )

            return

        save_json(
            CURRENT_TOPIC_FILE,
            selected
        )

        await update.message.reply_text(
            "⏳ جاري كتابة المقال...\n"
            "قد يستغرق دقيقة أو دقيقتين."
        )

        result = create_article(
            selected
        )

        if not result["success"]:

            await update.message.reply_text(
                "❌ فشل إنشاء المقال."
            )

            return

        article = result["data"]

        LAST_ARTICLE = article
        
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "👀 معاينة المقال",
                        callback_data="preview"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "📝 نشر المقال",
                        callback_data="publish"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "✏️ تعديل المقال",
                        callback_data="edit"
                    )
                ]
            ]
        )

        await update.message.reply_text(
            f"✅ تم إنشاء المقال\n\n"
            f"📌 {article['title']}\n\n"
            f"📝 {article['meta_description']}",
            reply_markup=keyboard
        )

        return

    # ==========================================
    # TEXT COMMANDS
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

            await update.message.reply_text(
                "✅ تم نشر المقال بنجاح."
            )

        else:

            await update.message.reply_text(
                "❌ فشل النشر."
            )

        return
        
    if text.lower() == "عدل":

        if LAST_ARTICLE is None:

            await update.message.reply_text(
                "❌ لا يوجد مقال."
            )

            return

        await update.message.reply_text(
            "✏️ ميزة التعديل سيتم إضافتها قريباً."
        )

        return

    await update.message.reply_text(
        "❌ أرسل رقم موضوع أو اكتب (انشر)."
    )

# ==========================================
# BUTTON HANDLER
# ==========================================

async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    global LAST_ARTICLE

    query = update.callback_query

    await query.answer()

    if LAST_ARTICLE is None:

        await query.edit_message_text(
            "❌ لا يوجد مقال."
        )

        return

    if query.data == "preview":

        article = LAST_ARTICLE.get(
            "article",
            ""
        )

        if len(article) > 3500:
            article = article[:3500] + "\n\n..."

        await query.message.reply_text(
            article
        )

        return
   if query.data == "publish":

            await query.edit_message_text(
            "🚀 جاري النشر على GitHub..."
        )

        success = publish_article(
            LAST_ARTICLE
        )

        if success:

            slug = LAST_ARTICLE.get(
                "slug",
                ""
            )

            await query.message.reply_text(
                f"✅ تم نشر المقال بنجاح.\n\n"
                f"📄 articles/{slug}.html"
            )

        else:

            await query.message.reply_text(
                "❌ فشل النشر على GitHub."
            )

        return
    if query.data == "edit":

        await query.edit_message_text(
            "✏️ ميزة التعديل سيتم إضافتها قريباً."
        )

        return

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

application.add_handler(
    CallbackQueryHandler(
        button_handler
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

# ==========================================
# ENTRY POINT
# ==========================================

if __name__ == "__main__":
    main()
