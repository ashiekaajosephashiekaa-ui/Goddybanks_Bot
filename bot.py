import os
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Token loaded from Railway environment variable (never hardcode it)
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

# Your admin's Telegram username (without @)
ADMIN_USERNAME = "Goddybanksss"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send welcome message with inline buttons when /start is issued."""
    keyboard = [
        [
            InlineKeyboardButton("🚀 Start", callback_data="start_action"),
            InlineKeyboardButton("📞 Contact Admin", url=f"https://t.me/{ADMIN_USERNAME}")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome_text = (
        "Welcome to GODDYBANKS_Bot\n"
        "Stay updated with trading insight, explore market analysis, "
        "understand trading strategies, and develop your skills with our trading community."
    )

    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle inline button presses."""
    query = update.callback_query
    await query.answer()

    if query.data == "start_action":
        await query.edit_message_text(
            text="You can join our channel here: https://t.me/Goddybanksss"
        )

def main() -> None:
    """Start the bot."""
    if not TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN environment variable not set.")

    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))

    application.run_polling()

if __name__ == "__main__":
    main()
