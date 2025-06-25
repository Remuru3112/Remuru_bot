
from flask import Flask, request
import telebot
import time
from openai import OpenAI

# 🔐 Telegram и OpenAI токены
API_TOKEN = '7894658829:AAHAul9aLv632y_EtlBviNSAby4GjylJ_KI'
OPENAI_API_KEY = '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'

# 🌐 Адрес вебхука
WEBHOOK_URL = 'https://remuru-bot.onrender.com'

# Инициализация
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)
client = OpenAI(api_key=OPENAI_API_KEY)

# Команда /start и /hello
@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Привет, я Remuru! Готов анализировать и озвучивать тексты.")

# Обработка текста
@bot.message_handler(content_types=['text'])
def handle_text(message):
    try:
        prompt = message.text
        time.sleep(1)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты помощник по имени Remuru, умный, ироничный и доброжелательный."},
                {"role": "user", "content": prompt}
            ]
        )
        reply = response.choices[0].message.content.strip()
        bot.reply_to(message, reply)
    except Exception as e:
        bot.reply_to(message, f"Ошибка при обработке запроса: {e}")

# Webhook обработчик
@app.route(f'/bot{API_TOKEN}', methods=['POST'])
def receive_update():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return 'OK', 200

# Страница-проверка
@app.route('/')
def index():
    return 'Бот Remuru работает! ✅', 200

# Запуск
if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url=f'{WEBHOOK_URL}/bot{API_TOKEN}')
    app.run(host='0.0.0.0', port=10000)
