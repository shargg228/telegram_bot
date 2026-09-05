import os

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, LabeledPrice
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    PreCheckoutQueryHandler,
    MessageHandler,
    filters
)

TOKEN = os.environ["TOKEN"]
PRICE = 10


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[
        InlineKeyboardButton(
            "📸 Отримати фото і відео — ⭐ 10",
            callback_data="buy"
        )
    ]]

    await update.message.reply_text(
        "Доступ до всіх фото та відео — ⭐ 10",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await query.message.reply_invoice(
        title="Фото + відео",
        description="Всі фото та відео",
        payload="content_10_stars",
        currency="XTR",
        prices=[LabeledPrice("Доступ до контенту", PRICE)]
    )


async def precheckout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.pre_checkout_query.answer(ok=True)


async def successful_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photos = [
        os.path.join("photos", f)
        for f in os.listdir("photos")
        if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))
    ]

    videos = [
        os.path.join("videos", f)
        for f in os.listdir("videos")
        if f.lower().endswith((".mp4", ".mov", ".mkv"))
    ]

    for photo in photos:
        with open(photo, "rb") as file:
            await update.message.reply_photo(photo=file)

    for video in videos:
        with open(video, "rb") as file:
            await update.message.reply_document(document=file)


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buy, pattern="^buy$"))
    app.add_handler(PreCheckoutQueryHandler(precheckout))
    app.add_handler(
        MessageHandler(
            filters.SUCCESSFUL_PAYMENT,
            successful_payment
        )
    )

    print("Бот запущений!")
    app.run_polling()


if __name__ == "__main__":
    main()
