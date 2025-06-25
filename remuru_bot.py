from flask import Flask, request
import telebot

# 🔐 Telegram API Token
API_TOKEN = '7894658829:AAHAul9aLv632y_EtlBviNSAby4GjylJ_KI'
WEBHOOK_URL = 'https://remuru-bot.onrender.com'

# Инициализация
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

@app.route(f'/bot{API_TOKEN}', methods=['POST'])
def receive_update():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return 'OK', 200

@app.route('/')
def index():
    return 'Bot is working!', 200

if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url=f'{WEBHOOK_URL}/bot{API_TOKEN}')
    app.run(host='0.0.0.0', port=10000)
