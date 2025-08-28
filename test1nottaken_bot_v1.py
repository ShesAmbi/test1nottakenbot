from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters, CallbackQueryHandler
TOKEN = "8397140327:AAGa5J6_BJiz9paPT4x3-MaVL7xsnG2PU6o"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hello! I’m alive.")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(update.message.text)


#create a menu with buttons
LESSONS = {
    "Gabbard": {
        " CHAPTER1 ": (

    "🧠*What Is Long-Term Psychodynamic Psychotherapy?*\n\n"
    "📖 *Key Concepts:*\n\n"
    "LT-PDP (Long-Term Psychodynamic Psychotherapy) focuses on unconscious processes and enduring personality change.\n\n"
    "⚡ *Core emphasis:*\n"
    "• transference\n"
    "• countertransference\n"
    "• interpretation\n"
    "• resistance\n"
    "• defense mechanisms\n\n"
    "🔄 Psychodynamic therapy differs from CBT in that it aims to alter personality structure, not just reduce symptoms.\n\n"
    "🧩 *Interpretation* is the most distinctive and essential intervention.\n\n"
    "📊 *Evidence:* Meta-analyses support long-term benefits of psychodynamic therapy across various disorders.\n\n"
    "💡 *Exam Pearl:* Most distinguishing feature = focus on transference and interpretation of unconscious conflict."


),


        "Chapter 2: Psychotherapy": "Text for psychotherapy...",
    },
    "Neuro Case": {
        "Chapter 1: Stroke": "Text about stroke...",
        "Chapter 2: Epilepsy": "Text about epilepsy...",
    },
}




async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(title, callback_data=f"topic|{title}")]
        for title in LESSONS.keys()
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # If called from a message (normal command)
    if update.message:
        await update.message.reply_text("📚 Select a topic:", reply_markup=reply_markup)
    # If called from a callback query (button press)
    elif update.callback_query:
        await update.callback_query.message.edit_text("📚 Select a topic:", reply_markup=reply_markup)


#handle button clicks

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # Acknowledge the button press

    data = query.data
    parts = data.split("|")

    # ----- Topic selected → show chapters -----
    if parts[0] == "topic":
        topic = parts[1]
        chapters_list = list(LESSONS[topic].keys())
        keyboard = [
            [InlineKeyboardButton(chap, callback_data=f"chapter|{topic}|{i}")]
            for i, chap in enumerate(chapters_list)
        ]
        keyboard.append([InlineKeyboardButton("⬅️ Back", callback_data="back|main")])
        await query.message.edit_text(
            f"📖 Chapters in {topic}:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )

    # ----- Chapter selected → show text -----
    elif parts[0] == "chapter":
        topic, index = parts[1], int(parts[2])
        chapters_list = list(LESSONS[topic].keys())
        chapter = chapters_list[index]
        text = LESSONS[topic][chapter]
        await query.message.edit_text(f"📄 {chapter}\n\n{text}", parse_mode="Markdown")



    # ----- Back button pressed -----
    elif parts[0] == "back":
        if parts[1] == "main":
            await menu(update, context)


def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()


if __name__ == "__main__":
    main()
