import telebot

from telebot import types

from geopy.geocoders import Nominatim

get_number = types.ReplyKeyboardMarkup(resize_keyboard=True)
get_number.add(types.KeyboardButton('Lokasiya',request_location=True))

bot = telebot.TeleBot("")

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id,"Assalomu alaykum!\nBotdan registratsiya o'tish uchun, botga lokasiyani yuboring",reply_markup=get_number)
    bot.register_next_step_handler(message,get_number_function)

def get_number_function(message):
    if message.location is None:
        bot.send_message(message.chat.id, "Iltimos, tugmani bosing",reply_markup=get_number)
        bot.register_next_step_handler(message,get_number_function)
    else:
        geolocator = Nominatim(user_agent="geoapiExercises") 
        location = geolocator.geocode(str(message.location.latitude)+","+str(message.location.longitude)) 
        bot.send_message(message.chat.id, f"Sizning joylashuvingiz haqida ma'lumot:\n{location}")

bot.polling()