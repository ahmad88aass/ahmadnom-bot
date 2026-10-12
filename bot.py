import os
import telebot
from telebot import types
from flask import Flask, request

TOKEN = "8936795820:AAFE9MM8zAHcQBX026lDi78Td5bcLghI8JE"
ADMIN_CHAT_ID = "8328829705"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

def notify_admin(text):
    try:
        bot.send_message(ADMIN_CHAT_ID, f"🚨 تقرير نشاط:\n{text}")
    except Exception as e:
        print(e)

@app.route('/webhook', methods=['POST'])
def webhook():
    return "OK", 200

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    username = message.from_user.username or "بدون معرف"
    
    notify_admin(f"👤 مستخدم جديد بدأ البوت:\nالمعرف: @{username}\nالايدي: {user_id}")

    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton("🔗 رابط الخدمة الأولى", callback_data="link_1")
    btn2 = types.InlineKeyboardButton("🌐 رابط الخدمة الثانية", callback_data="link_2")
    markup.add(btn1, btn2)
    
    bot.send_message(message.chat.id, "أهلاً بك. اختر الخدمة المطلوبة من الأسفل:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    user_id = call.from_user.id
    username = call.from_user.username or "بدون معرف"
    
    if call.data == "link_1":
        target_link = "https://example.com/service1"
        bot.answer_callback_query(call.id, "جاري جلب الطلب...")
        bot.send_message(call.message.chat.id, f"إليك الرابط الأول:\n{target_link}")
        notify_admin(f"📌 المستخدم @{username} (ID: {user_id}) طلب الرابط الأول.")
        
    elif call.data == "link_2":
        target_link = "https://example.com/service2"
        bot.answer_callback_query(call.id, "جاري جلب الطلب...")
        bot.send_message(call.message.chat.id, f"إليك الرابط الثاني:\n{target_link}")
        notify_admin(f"📌 المستخدم @{username} (ID: {user_id}) طلب الرابط الثاني.")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
