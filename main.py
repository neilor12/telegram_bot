from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)

from agent import LLM

TOKEN = "8081502126:AAFfxRxpx_FVlriQr5I3dTX89QdK6sS5nMk"

ASK = 1

keyboard = [["Задать вопрос", "Прорешать вариант", "Стоп"]]
markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Выберите действие:",
        reply_markup=markup
    )


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "Задать вопрос":
        await update.message.reply_text("Введите запрос")
        return ASK

    if text == "Прорешать вариант":
        await update.message.reply_text("Временно недоступно")


async def handle_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    # если пользователь решил нажать вторую кнопку
    if user_text == "Стоп":
        await update.message.reply_text("Больше вопросов не будет")
        return ConversationHandler.END

    await update.message.reply_text("Обрабатываю запрос...")

    answer = LLM(user_text)

    await update.message.reply_text(answer)

    await update.message.reply_text("Если хотите задать другой вопрос, введите его. Если хотите закончить, нажмите 'Стоп'.")

    # остаёмся в режиме вопросов
    return ASK

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    conv = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^Задать вопрос$"), menu)],
        states={
            ASK: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_question)]
        },
        fallbacks=[],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv)
    app.add_handler(MessageHandler(filters.Regex("^Прорешать вариант$"), menu))
    app.add_handler(MessageHandler(filters.Regex("^Стоп$"), menu))
    app.run_polling()


if __name__ == "__main__":
    main()