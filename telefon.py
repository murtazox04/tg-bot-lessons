import telebot

from telebot import types

get_number = types.ReplyKeyboardMarkup(resize_keyboard=True)
get_number.add(types.KeyboardButton('Telefon',request_contact=True))

bot = telebot.TeleBot("")

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id,"Assalomu alaykum!\nBotdan registratsiya o'tish uchun, botga telefon raqamingizni yuboring",reply_markup=get_number)
    bot.register_next_step_handler(message,get_number_function)

def get_number_function(message):
    if message.contact is None:
        bot.send_message(message.chat.id, "Iltimos, tugmani bosing",reply_markup=get_number)
        bot.register_next_step_handler(message,get_number_function)
    else:
        bot.send_message(message.chat.id, f"Sizning telefon raqamingiz: {str(message.contact.phone_number)}")

bot.polling()