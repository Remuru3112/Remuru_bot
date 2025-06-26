import os
from flask import Flask, request, jsonify
import requests
import openai
import pyttsx3

app = Flask(__name__)

# Получаем токены из переменных окружения
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

def generate_gpt_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150
    )
    return response.choices[0].message.content.strip()

def tts_speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        user_text = data["message"].get("text", "")
        bot_response = generate_gpt_response(user_text)
        send_message(chat_id, bot_response)
        print(f"Римуру говорит: {bot_response}")
        tts_speak(bot_response)
    return jsonify({"ok": True})

@app.route("/", methods=["GET"])
def home():
    return "RemuruBot is alive!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
