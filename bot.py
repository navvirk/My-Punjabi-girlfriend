import logging
import random
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# === Configuration ===
TOKEN = "7398804409:AAEl_rmFkjPCZlDx1H7Tz0AjmX-K5aPqG74"
WEBHOOK_URL = "https://punjabi-gf-bot.onrender.com"

GITHUB_USERNAME = "navvirk"
GITHUB_REPO = "My-Punjabi-girlfriend"
GITHUB_FILE = "romantic.txt"

# === Logging ===
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === Get a random romantic line ===
async def get_random_reply():
    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{GITHUB_REPO}/contents/{GITHUB_FILE}"
    headers = {"Accept": "application/vnd.github.v3.raw"}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        lines = response.text.strip().split("\n")
        return random.choice(lines)
    else:
        logger.error(f"GitHub error: {response.status_code}")
        return "Sorry jaan, GitHub ch kujh error aa gayi."

# === Reply to message ===
async def respond(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.text:
        logger.info(f"User: {update.message.from_user.username}, Message: {update.message.text}")
        reply = await get_random_reply()
        await update.message.reply_text(reply)

# === Start bot with webhook ===
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, respond))

    # Webhook
    app.run_webhook(
        listen="0.0.0.0",
        port=10000,
        webhook_url=WEBHOOK_URL
    )
