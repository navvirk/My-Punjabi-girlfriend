import requests
import random
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# === CONFIGURATION ===
TELEGRAM_TOKEN = "7398804409:AAEl_rmFkjPCZlDx1H7Tz0AjmX-K5aPqG74"
GITHUB_USERNAME = "navvirk"
GITHUB_REPO = "My-Punjabi-girlfriend"
GITHUB_FILE = "romantic.txt"
WEBHOOK_URL = "https://punjabi-gf-bot.onrender.com"  # e.g. https://your-render-url.onrender.com

async def get_random_reply():
    url = f"https://api.github.com/repos/virkxnav/My-Punjabi-girlfreind-/contents/romantic.txt"
    headers = {"Accept": "application/vnd.github.v3.raw"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        lines = response.text.strip().split("\n")
        return random.choice(lines)
    else:
        return "Sorry jaan, GitHub ch kujh error aa gayi."

async def respond(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply = await get_random_reply()
    await update.message.reply_text(reply)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), respond))

    # Set webhook
    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 8080)),
        webhook_url=WEBHOOK_URL
    )
