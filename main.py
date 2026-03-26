import os
import telebot
from flask import Flask
from openai import OpenAI
from threading import Thread

# --- Configuration ---
BOT_TOKEN = os.environ.get("BOT_TOKEN")
HF_TOKEN = os.environ.get("HF_TOKEN")

# Initialize Clients
bot = telebot.TeleBot(BOT_TOKEN)
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=HF_TOKEN,
)

app = Flask(__name__)

@app.route('/')
def home():
    return "JARVIS Bot is running!"

# --- Bot Logic ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "नमस्ते! मैं JARVIS हूँ। आप मुझसे कुछ भी पूछ सकते हैं।")

@bot.message_handler(func=lambda message: True)
def chat(message):
    try:
        # Chat completion request
        response = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-R1", # Using requested model
            messages=[
                {"role": "system", "content": "You are JARVIS. Respond in Hindi concisely."},
                {"role": "user", "content": message.text}
            ],
            temperature=0.7
        )
        reply = response.choices[0].message.content
        bot.reply_to(message, reply)
    except Exception as e:
        bot.reply_to(message, f"Error: {str(e)}")

# --- Server Start ---
def run_flask():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

if __name__ == "__main__":
    # Start Flask in a separate thread to keep Render happy
    Thread(target=run_flask).start()
    # Start the Telegram bot
    bot.infinity_polling()
