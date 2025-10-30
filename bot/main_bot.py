# bot_app.py
import os
import telebot
from settings.security import TOKEN_BOT

bot = telebot.TeleBot(TOKEN_BOT) #Mover de carpeta a main para que agarre bien el token

@bot.message_handler(commands=['contact'])
def start_handler(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, chat_id)

if __name__ == "__main__":
    print("Bot arrancando...")
    bot.infinity_polling()
