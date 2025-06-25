import telebot
from flask import Flask, request
import openai
import time

# 🔐 Telegram Bot Token и OpenAI API ключ
API_TOKEN = '7894658829:AAFS2tpJ942-UNkYGzETAuHaFdlyMeQ9beQ'
OPENAI_API_KEY = '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'

# 🌐 Webhook адрес (твой Render-домен без слэша на конце!)
WEBHOOK_URL = 'https://remuru-bot.onrender.com'

# Инициализация
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)
openai.api_key = OPENAI_API_KEY

# 📩 Команды бота
@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Привет, я Remuru! Готов анализировать и озвучивать тексты.")

# 💬 Текстовые сообщения
@bot.message_handler(content_types=['text'])
def handle_text(message):
    try:
        prompt = message.text
        # Задержка для Telegram API
        time.sleep(1)
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150
        )
        bot.reply_to(message, response.choices[0].text.strip())
    except Exception as e:
        bot.reply_to(message, f"Ошибка при обработке запроса: {e}")

# 📬 Webhook от Telegram
@app.route(f'/bot{API_TOKEN}', methods=['POST'])
def receive_update():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return 'OK', 200

# 🌐 Проверка работы
@app.route('/')
def index():
    return 'Бот Remuru работает! ✅', 200

# 🔧 Запуск
if __name__ == '__main__':
    # Устанавливаем Webhook при запуске
    bot.remove_webhook()
    bot.set_webhook(url=f'{WEBHOOK_URL}/bot{API_TOKEN}')
    app.run(host='0.0.0.0', port=10000)
