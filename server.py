from flask import Flask
from threading import Thread
from bible_game_bot import main

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Bible Bot is running 24/7 on Render!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

def start():
    Thread(target=run_flask).start()
    main()

if __name__ == "__main__":
    start()
