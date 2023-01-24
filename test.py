import asyncio
from pyrogram import Client, filters

from decouple import config

api_id = config('API_ID')
api_hash = config('API_HASH')
bot_token = config('TOKEN')

app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# async def main():
#     async with app:
#         await app.send_message("unnamed_userr", "Hi there! I'm using **Pyrogram**")

@app.on_message(filters.text and filters.private)
async def echo(client, message):
    await message.reply(message.text)
        
app.run()

