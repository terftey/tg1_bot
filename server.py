from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import logging
import asyncio
import threading

TOKEN = "7942972350:AAEvdIsOUbeQYYrorNcRwL-XIWm-B2VrFWw"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

app = Flask(__name__)

application = ApplicationBuilder().token(7942972350:AAEvdIsOUbeQYYrorNcRwL-XIWm-B2VrFWw).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I’m your Bible bot.")

application.add_handler(CommandHandler("start", start))

@app.route('/')
def home():
    return "Bible Bot is running!"

@app.route(f'/{TOKEN}', methods=['POST'])
async def webhook():
    await application.initialize()
    await application.process_update(Update.de_json(request.get_json(force=True), application.bot))
    return 'OK'

if __name__ == '__main__':
    async def set_webhook():
        await application.bot.set_webhook(f"https://tg1-bot.onrender.com/{7942972350:AAEvdIsOUbeQYYrorNcRwL-XIWm-B2VrFWw}")

    def run_flask():
        app.run(host='0.0.0.0', port=8080)

    threading.Thread(target=run_flask).start()
    asyncio.run(set_webhook())

