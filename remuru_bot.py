import openai
import telebot
import time
from flask import Flask, request

# 🔐 Telegram и OpenAI токены
API_TOKEN = '7894658829:AAFS2tpJ942-UNkYGzETAuHaFdlyMeQ9beQ'
OPENAI_API_KEY = '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'

# 🌐 Адрес вебхука
WEBHOOK_URL = 'https://remuru-bot.onrender.com'

# Инициализация
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)
openai.api_key = OPENAI_API_KEY

# Команда /start и /hello
@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Привет, я Remuru! Готов анализировать и озвучивать тексты.")

# Обработка текста
@bot.message_handler(content_types=['text'])
def handle_text(message):
    try:
        prompt = message.text
        time.sleep(1)  # Задержка для Telegram API

        # Новый запрос с использованием tools и web_search_preview
        response = openai.ChatCompletion.create(
            model="gpt-4.1",  # Используем GPT-4.1
            messages=[
                {"role": "system", "content": "Ты помощник по имени Remuru, умный, ироничный и доброжелательный."},
                {"role": "user", "content": prompt}
            ],
            tools=[
                {"type": "web_search_preview", "input": "What was a positive news story from today?"}
            ]
        )

        reply = response['choices'][0]['message']['content'].strip()
        bot.reply_to(message, reply)

    except openai.error.AuthenticationError as e:
        print(f"Ошибка авторизации: {e}")
        bot.reply_to(message, "Ошибка авторизации с OpenAI. Проверьте API-ключ.")
    except Exception as e:
        print(f"Общая ошибка: {e}")
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
