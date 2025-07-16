import logging
from telegram import ForceReply, Update
import requests
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
import json
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
    )
    usernames = []
    first_name = user.first_name or ""
    last_name = user.last_name or ""
    username = user.username if user.username else f"{first_name} {last_name}".strip()
    if username not in usernames:
        usernames.append(username)
    with open("usernames.json","wt") as f1:
        f1.write(json.dumps(usernames))
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Help!")
    user = update.effective_user
    usernames = []
    first_name = user.first_name or ""
    last_name = user.last_name or ""
    username = user.username if user.username else f"{first_name} {last_name}".strip()
    try:
        with open("usernames.json", "r", encoding="utf-8") as f:
            usernames = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        usernames = []
    if username not in usernames:
        usernames.append(username)
        with open("usernames.json", "w", encoding="utf-8") as f:
            json.dump(usernames, f, ensure_ascii=False, indent=4)
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.text == "hi":
        await update.message.reply_text("hello friend")
    elif update.message.text == "bye":
        await update.message.reply_text("bye")
    else:
        await update.message.reply_text(update.message.text)
    user = update.effective_user
    first_name = user.first_name or ""
    last_name = user.last_name or ""
    username = user.username if user.username else f"{first_name} {last_name}".strip()
    try:
        with open("usernames.json", "r", encoding="utf-8") as f:
            usernames = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        usernames = []
    if username not in usernames:
        usernames.append(username)
        with open("usernames.json", "w", encoding="utf-8") as f:
            json.dump(usernames, f, ensure_ascii=False, indent=4)
def main() -> None:
    application = Application.builder().token("7737988161:AAHSiBYPtgDXJuxnY6FjA2L6n-yvqvw3npg").build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()