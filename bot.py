import os
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.error import BadRequest
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# ============================================================
#  CONFIG
# ============================================================
TOKEN          = os.environ.get("TELEGRAM_BOT_TOKEN")
ADMIN_USERNAME = "Goddybanksss"
CHANNEL_URL    = "https://t.me/Goddybanksss"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
log = logging.getLogger(__name__)

# ============================================================
#  TEXT BLOCKS
# ============================================================
HOME_TEXT = (
    "<b>GODDYBANKS</b>\n"
    "<i>Trading Intelligence & Market Insight</i>\n"
    "━━━━━━━━━━━━━━━━━━━━━━\n\n"
    "Welcome to the official bot for the <b>Goddybanks</b> community.\n\n"
    "Access curated insights, market analysis, and educational "
    "resources — all in one place.\n\n"
    "<i>Select a section below to begin.</i>"
)

INSIGHTS_TEXT = (
    "<b>Trading Insights</b>\n"
    "━━━━━━━━━━━━━━━━━━━━━━\n\n"
    "Curated observations and commentary from the markets.\n\n"
    "Choose a topic:"
)

ANALYSIS_TEXT = (
    "<b>Market Analysis</b>\n"
    "━━━━━━━━━━━━━━━━━━━━━━\n\n"
    "Structured breakdowns of price action and key levels.\n\n"
    "Choose a timeframe:"
)

STRATEGIES_TEXT = (
    "<b>Trading Strategies</b>\n"
    "━━━━━━━━━━━━━━━━━━━━━━\n\n"
    "Frameworks and playbooks used inside the community.\n\n"
    "Choose a category:"
)

RESOURCES_TEXT = (
    "<b>Tools & Resources</b>\n"
    "━━━━━━━━━━━━━━━━━━━━━━\n\n"
    "Hand-picked material to sharpen your trading.\n\n"
    "Choose a category:"
)

ABOUT_TEXT = (
    "<b>About GODDYBANKS</b>\n"
    "━━━━━━━━━━━━━━━━━━━━━━\n\n"
    "An independent trading community built on discipline, "
    "education, and market structure.\n\n"
    "<b>Focus areas</b>\n"
    "› Market structure & price action\n"
    "› Risk management principles\n"
    "› Strategy development\n"
    "› Trading psychology\n\n"
    "<i>For collaborations or enquiries, use the contact button below.</i>"
)

SUPPORT_TEXT = (
    "<b>Support</b>\n"
    "━━━━━━━━━━━━━━━━━━━━━━\n\n"
    "Need assistance? The admin is one tap away.\n\n"
    "<i>Please allow up to 24 hours for a response.</i>"
)

PLACEHOLDER_TEXT = (
    "<b>Coming Soon</b>\n"
    "━━━━━━━━━━━━━━━━━━━━━━\n\n"
    "This section is being prepared. In the meantime, "
    "join the channel for the latest updates.\n"
)

# ============================================================
#  KEYBOARD BUILDERS
# ============================================================
def back_row(target: str = "menu"):
    """Single back button used on every sub-screen."""
    return [InlineKeyboardButton("‹  Back", callback_data=target)]


def home_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        # Primary call-to-action
        [InlineKeyboardButton("📢  Join Our Channel", url=CHANNEL_URL)],

        # Categories (2-column grid)
        [
            InlineKeyboardButton("📈  Trading Insights", callback_data="insights"),
            InlineKeyboardButton("📊  Market Analysis",  callback_data="analysis"),
        ],
        [
            InlineKeyboardButton("🧠  Strategies",       callback_data="strategies"),
            InlineKeyboardButton("🛠  Resources",        callback_data="resources"),
        ],
        [
            InlineKeyboardButton("ℹ️  About",            callback_data="about"),
            InlineKeyboardButton("💬  Support",          callback_data="support"),
        ],

        # Contact admin (direct link)
        [InlineKeyboardButton("✉️  Contact Admin", url=f"https://t.me/{ADMIN_USERNAME}")],
    ])


def insights_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📚  Educational Content", callback_data="placeholder"),
            InlineKeyboardButton("🔔  Trade Alerts",        callback_data="placeholder"),
        ],
        [InlineKeyboardButton("📢  Join Channel", url=CHANNEL_URL)],
        back_row(),
    ])


def analysis_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📈  Daily Analysis",  callback_data="placeholder"),
            InlineKeyboardButton("📉  Weekly Outlook",  callback_data="placeholder"),
        ],
        [InlineKeyboardButton("📢  Join Channel", url=CHANNEL_URL)],
        back_row(),
    ])


def strategies_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🌱  Beginner",      callback_data="placeholder"),
            InlineKeyboardButton("⚙️  Intermediate",  callback_data="placeholder"),
        ],
        [InlineKeyboardButton("🎯  Advanced",        callback_data="placeholder")],
        [InlineKeyboardButton("📢  Join Channel", url=CHANNEL_URL)],
        back_row(),
    ])


def resources_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📘  Guides",       callback_data="placeholder"),
            InlineKeyboardButton("🧰  Tools",        callback_data="placeholder"),
        ],
        [InlineKeyboardButton("📢  Join Channel", url=CHANNEL_URL)],
        back_row(),
    ])


def about_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📢  Join Channel",   url=CHANNEL_URL)],
        [InlineKeyboardButton("✉️  Contact Admin", url=f"https://t.me/{ADMIN_USERNAME}")],
        back_row(),
    ])


def support_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✉️  Contact Admin", url=f"https://t.me/{ADMIN_USERNAME}")],
        [InlineKeyboardButton("📢  Join Channel",  url=CHANNEL_URL)],
        back_row(),
    ])


# ============================================================
#  SAFE EDIT HELPER
# ============================================================
async def safe_edit(query, text: str, markup: InlineKeyboardMarkup) -> None:
    """Edit the message, ignoring the 'message not modified' error."""
    try:
        await query.edit_message_text(
            text=text,
            reply_markup=markup,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True,
        )
    except BadRequest as e:
        if "Message is not modified" not in str(e):
            raise


# ============================================================
#  HANDLERS
# ============================================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        HOME_TEXT,
        reply_markup=home_keyboard(),
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await start(update, context)


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    data = query.data

    routes = {
        "menu":       (HOME_TEXT,       home_keyboard),
        "insights":   (INSIGHTS_TEXT,   insights_keyboard),
        "analysis":   (ANALYSIS_TEXT,   analysis_keyboard),
        "strategies": (STRATEGIES_TEXT, strategies_keyboard),
        "resources":  (RESOURCES_TEXT,  resources_keyboard),
        "about":      (ABOUT_TEXT,      about_keyboard),
        "support":    (SUPPORT_TEXT,    support_keyboard),
        "placeholder":(PLACEHOLDER_TEXT, lambda: InlineKeyboardMarkup([
            [InlineKeyboardButton("📢  Join Channel", url=CHANNEL_URL)],
            back_row(),
        ])),
    }

    text, builder = routes.get(data, (HOME_TEXT, home_keyboard))
    await safe_edit(query, text, builder())


# ============================================================
#  MAIN
# ============================================================
def main() -> None:
    if not TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN environment variable not set.")

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help",  help_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()


if __name__ == "__main__":
    main()
