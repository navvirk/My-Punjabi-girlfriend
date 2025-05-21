import logging
import random
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# === CONFIGURATION ===
TOKEN = "7398804409:AAEl_rmFkjPCZlDx1H7Tz0AjmX-K5aPqG74"
WEBHOOK_URL = "https://punjabi-gf-bot.onrender.com"

GITHUB_USERNAME = "navvirk"
GITHUB_REPO = "My-Punjabi-girlfriend"
GITHUB_FILE = "romantic.txt"

# === Logging (optional but helpful for debugging) ===
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === GitHub Reader ===
async def get_random_reply():
    url = f"https://api.github.com/repos/navvirk/My-Punjabi-girlfriend/contents/romantic.txt"
    headers = {"Accept": "application/vnd.github.v3.raw"}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        lines = response.text.strip().split("\n")
        return random.choice(lines)
    else:
        return "Sorry jaan, GitHub ch kujh error aa gayi."

# === Telegram Response ===
async def respond(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"User said: {update.message.text}")
    reply = await get_random_reply()
    await update.message.reply_text(reply)

# === Main App Setup ===
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, respond))
    
    # RUN AS WEBHOOK
    app.run_webhook(
        listen="0.0.0.0",
        port=10000,
        webhook_url=WEBHOOK_URL
    )
