import pyrogram
from pyrogram import Client, filters

from decouple import config

api_id = config('API_ID')
api_hash = config('API_HASH')
bot_token = config('TOKEN')

app = Client("my_account", api_id=api_id, api_hash=api_hash)

@app.on_message(pyrogram.filters.private)
def echo_message_test(client, message):
    text = "Biror habar yuboring!"
    app.send_message(chat_id='@text_to_audiobot', text=text)

@app.on_message(pyrogram.filters.private)
def echo_message(client, message):
    client.send_message(chat_id='@text_to_audiobot', text=message.text)

app.run()
