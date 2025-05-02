from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, CallbackContext
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "7942972350:AAEvdIsOUbeQYYrorNcRwL-XIWm-B2VrFWw"  # Your bot token here
bot = Bot(token=TOKEN)

app = Flask(__name__)

dispatcher = Dispatcher(bot, None, workers=0, use_context=True)

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Hello! I’m your Bible bot.")

dispatcher.add_handler(CommandHandler("start", start))

@app.route('/')
def index():
    return 'Bot is running!'

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return 'OK'

if __name__ == '__main__':
    # Set the webhook for Telegram to reach the bot
    bot.setWebhook(f"https://tg1-bot.onrender.com/{TOKEN}")
    app.run(host='0.0.0.0', port=8080)  # Running the server on port 8080
