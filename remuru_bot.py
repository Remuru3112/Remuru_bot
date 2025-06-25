
from flask import Flask, request
import telebot
import openai

# API tokens
API_TOKEN = '7894658829:AAHq2EWIkde3KGubcafgmE9iRzWGewRN-b4'
OPENAI_API_KEY = 'sk-proj-RNiJdvn0u2IeF7A644bls7STbJtVF8h_fqZ1Z5s0XsJWTnK7wjjxsB'

# Initialize bot and Flask app
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# OpenAI setup
openai.api_key = OPENAI_API_KEY

# Handlers
@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Привет, я Remuru! Готов к анализу и озвучке.")

@bot.message_handler(content_types=['text'])
def handle_text(message):
    prompt = message.text
    response = openai.Completion.create(
        engine="text-davinci-003",  # Or any other GPT model
        prompt=prompt,
        max_tokens=150
    )
    bot.reply_to(message, response.choices[0].text.strip())

# Webhook handler
@app.route('/' + API_TOKEN, methods=['POST'])
def webhook():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@app.route("/")
def index():
    return "Бот Remuru запущен!", 200

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url='https://ТВОЙ_АДРЕС_РЕНДЕР/renderbot')  # Подставь свой адрес Render
    app.run(host="0.0.0.0", port=10000)
