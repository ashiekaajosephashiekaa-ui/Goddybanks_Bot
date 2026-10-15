import os
import logging
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
ADMIN_USERNAME = "Goddybanksss"          # without @
CHANNEL_URL = "https://t.me/Goddybanksss"  # your channel link

# ---------- Main Menu ----------
def main_menu_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton("📢 Join Channel", url=CHANNEL_URL),
        ],
        [
            InlineKeyboardButton("📈 Trading Insights", callback_data="trading_insights"),
            InlineKeyboardButton("📊 Market Analysis", callback_data="market_analysis"),
        ],
        [
            InlineKeyboardButton("🧠 Strategies", callback_data="strategies"),
            InlineKeyboardButton("🛠️ Tools & Resources", callback_data="tools"),
        ],
        [
            InlineKeyboardButton("📞 Contact Admin", url=f"https://t.me/{ADMIN_USERNAME}"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


WELCOME_TEXT = (
    "**Welcome to GODDYBANKS_Bot**\n\n"
    "Stay updated with trading insight, explore market analysis, "
    "understand trading strategies, and develop your skills with our trading community.\n\n"
    "Choose an option below:"
)


# ---------- /start ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        WELCOME_TEXT,
        reply_markup=main_menu_keyboard(),
        parse_mode="Markdown",
    )


# ---------- Button Handler ----------
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == "trading_insights":
        sub_keyboard = [
            [InlineKeyboardButton("📚 Educational Content", callback_data="edu_content")],
            [InlineKeyboardButton("🔔 Trade Alerts", callback_data="trade_alerts")],
            [InlineKeyboardButton("📢 Join Channel", url=CHANNEL_URL)],
            [InlineKeyboardButton("⬅️ Back", callback_data="main_menu")],
        ]
        await query.edit_message_text(
            text="**Trading Insights**\nSelect a topic:",
            reply_markup=InlineKeyboardMarkup(sub_keyboard),
            parse_mode="Markdown",
        )

    elif query.data == "market_analysis":
        sub_keyboard = [
            [InlineKeyboardButton("📈 Daily Analysis", callback_data="daily_analysis")],
            [InlineKeyboardButton("📉 Weekly Outlook", callback_data="weekly_outlook")],
            [InlineKeyboardButton("📢 Join Channel", url=CHANNEL_URL)],
            [InlineKeyboardButton("⬅️ Back", callback_data="main_menu")],
        ]
        await query.edit_message_text(
            text="**Market Analysis**\nSelect a topic:",
            reply_markup=InlineKeyboardMarkup(sub_keyboard),
            parse_mode="Markdown",
        )

    elif query.data == "strategies":
        await query.edit_message_text(
            text="**Strategies**\nDetailed strategies are posted in our channel.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📢 Join Channel", url=CHANNEL_URL)],
                [InlineKeyboardButton("⬅️ Back", callback_data="main_menu")],
            ]),
            parse_mode="Markdown",
        )

    elif query.data == "tools":
        await query.edit_message_text(
            text="**Tools & Resources**\nComing soon.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📢 Join Channel", url=CHANNEL_URL)],
                [InlineKeyboardButton("⬅️ Back", callback_data="main_menu")],
            ]),
            parse_mode="Markdown",
        )

    elif query.data == "main_menu":
        await query.edit_message_text(
            text=WELCOME_TEXT,
            reply_markup=main_menu_keyboard(),
            parse_mode="Markdown",
        )

    else:
        # Placeholder for other sub-buttons
        await query.edit_message_text(
            text="More content coming soon. Stay tuned!",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📢 Join Channel", url=CHANNEL_URL)],
                [InlineKeyboardButton("⬅️ Back", callback_data="main_menu")],
            ]),
            parse_mode="Markdown",
        )


# ---------- main ----------
def main() -> None:
    if not TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN environment variable not set.")

    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))

    application.run_polling()


if __name__ == "__main__":
    main()
