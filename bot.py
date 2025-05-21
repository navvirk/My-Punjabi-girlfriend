import os
import random
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from aiohttp import web

# === CONFIGURATION ===
TELEGRAM_TOKEN = "7398804409:AAEl_rmFkjPCZlDx1H7Tz0AjmX-K5aPqG74"
GITHUB_USERNAME = "navvirk"
GITHUB_REPO = "My-Punjabi-girlfriend"
GITHUB_FILE = "romantic.txt"

# === BOT LOGIC ===
async def get_random_reply():
    url = f"https://api.github.com/repos/navvirk/My-Punjabi-girlfreind/contents/bot.py"
    headers = {"Accept": "application/vnd.github.v3.raw"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        lines = response.text.strip().split("\n")
        return random.choice(lines) if lines else "Jaan, file ch kujh vi nahi likheya."
    else:
        return "Sorry jaan, GitHub ch kujh error aa gayi."

async def respond(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply = await get_random_reply()
    await update.message.reply_text(reply)

# === WEB SERVER SETUP ===
async def handle_root(request):
    return web.Response(text="Bot is alive!")

async def handle_webhook(request):
    update = Update.de_json(await request.json(), app.bot)
    await app.update_queue.put(update)
    return web.Response()

# === STARTUP ===
if __name__ == "__main__":
    import asyncio

    app = ApplicationBuilder().token "7398804409:AAEl_rmFkjPCZlDx1H7Tz0AjmX-K5aPqG74.build"()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, respond))

    async def run():
        runner = web.AppRunner(web.Application())
        await runner.setup()

        # add routes
        runner.app.router.add_get("/", handle_root)
        runner.app.router.add_post("/webhook", handle_webhook)

        site = web.TCPSite(runner, "0.0.0.0", port=int(os.environ.get("PORT", 10000)))
        await app.initialize()
        await site.start()
        print("Bot is running...")
        await app.start()
        await app.updater.start_polling()
        await app.updater.idle()

    asyncio.run(run())
