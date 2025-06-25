import telebot
import openai
import time
from flask import Flask, request
from queue import Queue
from threading import Thread

# Токен Telegram-бота от BotFather
API_TOKEN = '7894658829:AAFS2tpJ942-UNkYGzETAuHaFdlyMeQ9beQ'

# Ключ OpenAI (если используете OpenAI)
OPENAI_API_KEY = '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'

# Инициализация бота и Flask приложения
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# Настройка OpenAI API
openai.api_key = OPENAI_API_KEY

# Очередь для обработки сообщений
message_queue = Queue()

def process_message():
    while True:
        message = message_queue.get()
        if message:
            prompt = message.text
            response = openai.Completion.create(
                engine="text-davinci-003",  # Или любой другой GPT-3/4
                prompt=prompt,
                max_tokens=150
            )
            bot.reply_to(message, response.choices[0].text.strip())
            time.sleep(1)  # Пауза между запросами

# Поток для обработки очереди
thread = Thread(target=process_message)
thread.daemon = True
thread.start()

# Обработчик команды /start и /hello
@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Привет, я Remuru! Готов к анализу и озвучке.")

# Обработчик текстовых сообщений
@bot.message_handler(content_types=['text'])
def handle_text(message):
    message_queue.put(message)  # Добавляем сообщение в очередь для обработки

# Установка вебхука
bot.remove_webhook()
bot.set_webhook(url='https://remuru-bot.onrender.com/bot7894658829:AAFS2tpJ942-UNkYGzETAuHaFdlyMeQ9beQ')

# Обработчик webhook
@app.route('/' + API_TOKEN, methods=['POST'])
def webhook():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

# Главная страница
@app.route("/")
def index():
    return "Бот Remuru запущен!", 200

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url='https://remuru-bot.onrender.com/bot7894658829:AAFS2tpJ942-UNkYGzETAuHaFdlyMeQ9beQ')
    app.run(host="0.0.0.0", port=10000)
