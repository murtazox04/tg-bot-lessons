import time

from aiogram import Dispatcher, Bot, executor
from aiogram.types import Message

from connection import create_db, database_query, send_users

create_db()

bot = Bot(token="1635016850:AAHjfthCC4JHWTUdReWRQyyV5HxSG-Wx4Vk")

dp = Dispatcher(bot)

user_id_required = 1767432724


@dp.message_handler(commands=['start'])
async def welcome(message: Message):
    await bot.send_message(message.chat.id, "Salom dunyo")
    get_is_there = database_query("SELECT * FROM user_info WHERE user_id = ?", (message.from_user.id,))
    print(get_is_there)
    if get_is_there == []:
        database_query(f"INSERT INTO user_info VALUES(?,?)", (message.from_user.id, message.from_user.first_name,))


@dp.message_handler(commands=['send_users'])
async def handler3(message: Message):
    if message.from_user.id == user_id_required:
        get_all_users = send_users("SELECT * FROM user_info WHERE user_id",)
        usrs = 0

        for tt in get_all_users:
            try:
                usrs += 1
                await bot.copy_message(tt[0], message.chat.id, message.reply_to_message.message_id)
                time.sleep(.05)
            except:
                usrs = usrs - 1
            print(usrs)
            await bot.send_message(message.chat.id, f"done. sent to users: {str(usrs)}")

if __name__ == '__main__':
    executor.start_polling(dp)
