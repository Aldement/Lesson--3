import telebot # библиотека telebot
from config import token # импорт токена

bot = telebot.TeleBot(token) 

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Я бот для управления чатом.")

@bot.message_handler(commands=['ban'])
def ban_user(message):
    if message.reply_to_message: #проверка на то, что эта команда была вызвана в ответ на сообщение 
        chat_id = message.chat.id # сохранение id чата
         # сохранение id и статуса пользователя, отправившего сообщение
        user_id = message.reply_to_message.from_user.id
        user_status = bot.get_chat_member(chat_id, user_id).status 
         # проверка пользователя
        if user_status == 'administrator' or user_status == 'creator':
            bot.reply_to(message, "Невозможно забанить администратора.")
        else:
            bot.ban_chat_member(chat_id, user_id) # пользователь с user_id будет забанен в чате с chat_id
            bot.reply_to(message, f"Пользователь @{message.reply_to_message.from_user.username} был забанен.")
    else:
        bot.reply_to(message, "Эта команда должна быть использована в ответ на сообщение пользователя, которого вы хотите забанить.")

@bot.message_handler(commands=['unban'])
def unban_user(message):
    if message.reply_to_message:  # проверка на то, что команда была вызвана в ответ на сообщение
        chat_id = message.chat.id  # сохранение id чата
        # сохранение id пользователя, которого нужно разбанить
        user_id = message.reply_to_message.from_user.id
        
        try:
            # разбанить пользователя в чате
            bot.unban_chat_member(chat_id, user_id)
            bot.reply_to(message, f"Пользователь @{message.reply_to_message.from_user.username} был разбанен.")
        except Exception as e:
            bot.reply_to(message, f"Произошла ошибка: {e}")
    else:
        bot.reply_to(message, "Эта команда должна быть использована в ответ на сообщение пользователя, которого вы хотите разбанить.")

@bot.message_handler(func=lambda message: True)
def check_message(message):
    if "https://" in message.text:  
        chat_id = message.chat.id  
        user_id = message.from_user.id  
        username = message.from_user.username  
        first_name = message.from_user.first_name  
        last_name = message.from_user.last_name  
        
        user_info = f"User: @{username}, ID: {user_id}, First Name: {first_name}, Last Name: {last_name}"
        print(user_info) 

        try:
            # бан пользователя
            bot.ban_chat_member(chat_id, user_id)
            bot.reply_to(message, f"Пользователь @{username} был забанен за отправку ссылки.")
        except Exception as e:
            bot.reply_to(message, f"Произошла ошибка при бане пользователя: {e}")
    else:
        # если ссылки нет, просто продолжаем работу бота
        bot.reply_to(message, "Сообщение не содержит ссылку, никаких действий не требуется.")

@bot.message_handler(content_types=['new_chat_members'])
def make_some(message):
    bot.send_message(message.chat.id, 'I accepted a new user!')
    bot.approve_chat_join_request(message.chat.id, message.from_user.id)

bot.infinity_polling(none_stop=True)
