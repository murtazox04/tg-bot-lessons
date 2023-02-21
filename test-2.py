# Import libraries
from typing import Optional
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import re
import json
import requests
import pymongo
import logging
import time
from pyromod import listen
from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime
import locale
import numpy
import certifi
from decouple import config

log = logging.getLogger(__name__)

# Telegram bot client
client = Client("Telegram",
                api_id=config("API_ID"),
                api_hash=config("API_HASH"),
                bot_token=config("TOKEN"))

# ============================================================================
client_db = pymongo.MongoClient(
    "mongodb+srv://murtazo:<murtazo1280>@cluster0.dsybecf.mongodb.net/?retryWrites=true&w=majority")
db = client_db['murtazo']
collection_bot = db['bot']



# ============================================================================
@client.on_message(filters.command("start"))
async def start(_, message):
    await message.reply_text(f"Hello!", quote=True)


# ============================================================================
@client.on_message(filters.command("newsignal") & filters.private)
async def new_signal(_, message):
    log.info("Enter inside new_signal method")
    if "true" == "true":

        # ============================================================================
        chat_id = message.from_user.id
        identifier = (message.chat.id, message.from_user.id, message.id)
        print(chat_id)
        s_pair = await client.ask(
            identifier=identifier,
            text=f'Which Pair you want to send the signal ?\n • for example: ETHUSDT',
            filters=None, timeout=60)
        s_type = await client.ask(
            identifier=identifier, f'You want to go long or short ?\n • for example: Long', 
            filters=None, timeout=60)
        s_levarage = await client.ask(
            identifier=identifier, f'Tell me amount of leverage?\n • for example: 50', 
            filters=None, timeout=60)
        s_entry = await client.ask(
            identifier=identifier, f'Tell me amount of ENTRY?\n • for example: 1500', 
            filters=None, timeout=60)
        s_sl = await client.ask(
            identifier=identifier, f'Tell me amount of Stop loss ?\n • for example: 1200', 
            filters=None, timeout=60)
        s_tp = await client.ask(
            identifier=identifier, f'Tell me tp ideal goal ?\n • for example: 2', 
            filters=None, timeout=60)
        s_budget = await client.ask(
            identifier=identifier, f'Tell me amount of Budget ?\n • for example: 5 or 2.5', 
            filters=None, timeout=60)
        s_percentage = await client.ask(
            identifier=identifier,
            f'(Optional) Tell me amount of Percentage of oscillation ?\n • for example: 0.5 or 1',
            filters=None, timeout=60)
        # ============================================================================
        log.info("Acquire all inputs")

        pair = s_pair.text
        pair = pair.upper()
        type = s_type.text
        type = type.upper()
        levarage = s_levarage.text
        entry = s_entry.text
        sl = s_sl.text
        tp = s_tp.text
        budget = s_budget.text
        s_percentage = s_percentage.text
        s_percentage = s_percentage.strip()
        tp_array = []

        if not s_percentage:
            percentage = float(1)
        else:
            percentage = float(s_percentage)

        # ============================================================================
        if type.lower() == "short":
            rel = float(entry)
            tp_one = f"{round(rel - rel * (percentage * 1) / 100, 6)}"
            tp_two = f"{round(rel - rel * (percentage * 2) / 100, 6)}"
            tp_three = f"{round(rel - rel * (percentage * 3) / 100, 6)}"
            tp_four = f"{round(rel - rel * (percentage * 4) / 100, 6)}"
            tp_five = f"{round(rel - rel * (percentage * 5) / 100, 6)}"
            tp_six = f"{round(rel - rel * (percentage * 6) / 100, 6)}"
            tp_seven = f"{round(rel - rel * (percentage * 7) / 100, 6)}"
            tp_eight = f"{round(rel - rel * (percentage * 8) / 100, 6)}"
            tp_nine = f"{round(rel - rel * (percentage * 9) / 100, 6)}"
            tp_ten = f"{round(rel - rel * (percentage * 10) / 100, 6)}"
            tp_array = numpy.array([
                tp_one, tp_two, tp_three, tp_four, tp_five,
                tp_six, tp_seven, tp_eight, tp_nine, tp_ten
                ])

        # ============================================================================
        if type.lower() == "long":
            rel = float(entry)
            tp_one = f"{round(rel * (percentage * 1) / 100 + rel, 6)}"
            tp_two = f"{round(rel * (percentage * 2) / 100 + rel, 6)}"
            tp_three = f"{round(rel * (percentage * 3) / 100 + rel, 6)}"
            tp_four = f"{round(rel * (percentage * 4) / 100 + rel, 6)}"
            tp_five = f"{round(rel * (percentage * 5) / 100 + rel, 6)}"
            tp_six = f"{round(rel * (percentage * 6) / 100 + rel, 6)}"
            tp_seven = f"{round(rel * (percentage * 7) / 100 + rel, 6)}"
            tp_eight = f"{round(rel * (percentage * 8) / 100 + rel, 6)}"
            tp_nine = f"{round(rel * (percentage * 9) / 100 + rel, 6)}"
            tp_ten = f"{round(rel * (percentage * 10) / 100 + rel, 6)}"
            tp_array = numpy.array([
                tp_one, tp_two, tp_three, tp_four, tp_five,
                tp_six, tp_seven, tp_eight, tp_nine, tp_ten
                ])

        log.info("tp_array ", tp_array)

        # httpClient = requests.Session()
        url = "https://nebulous-crown-production-d964.up.railway.app/order/"  # spring


        payload = {
            "ticker": str(pair),
            "order_type": str(type).lower(),
            "limitt": str(entry),
            "amount_perc": str(budget),
            "leverage": str(levarage),
            "takeprofit": str(tp),
            "stoploss": str(sl),
            "oscillation": str(percentage)
        }
        print(payload)

        headers = {'Content-type': 'application/json'}
        print(headers)
        requests.post(url, data=json.dumps(payload), headers=headers)
        # check if error non aggiunge segnale nei gruppi e nemmeno in mongo


        signal_message_prem = f"**{pair}**\n(**{type} {levarage}x**)\n\n**ENTRY**: {entry}\n\n**TAKE PROFIT**:\nTarget 1: {tp_one}\nTarget 2: {tp_two}\nTarget 3: {tp_three}\nTarget 4: {tp_four}\nTarget 5: {tp_five}\nTarget 6: {tp_six}\nTarget 7: {tp_seven}\nTarget 8: {tp_eight}\nTarget 9: {tp_nine}\nTarget 10: {tp_ten}\n\n**STOP LOSS**: {sl}\n\n\n🚀**PREMIUM**\n\n**BUDGET**: {budget}%\n**TP**: {tp}"
        signal_message_basic = f"**{pair}**\n(**{type} {levarage}x**)\n\n**ENTRY**: {entry}\n\n**TAKE PROFIT**:\nTarget 1: {tp_one}\nTarget 2: {tp_two}\nTarget 3: {tp_three}\nTarget 4: {tp_four}\nTarget 5: {tp_five}\nTarget 6: {tp_six}\nTarget 7: {tp_seven}\nTarget 8: {tp_eight}\nTarget 9: {tp_nine}\nTarget 10: {tp_ten}\n\n**STOP LOSS**: {sl}"
        signal_message_groups_bot = f"Nuova posizione aperta sulla moneta **{pair}**\n\nPer qualsiasi problema, dubbio o domanda contattare il proprio tutor."


        # ============================================================================
        kkj_prem = await client.send_message(
            chat_id=Config.prem_chat,
            text=signal_message_prem)
        ms_id_prem = kkj_prem.id

        log.info("message on premium group sent")

        kkj_basic = await client.send_message(
            chat_id=Config.basic_chat,
            text=signal_message_basic)
        ms_id_basic = kkj_basic.id

        log.info("message on basic group sent")
        # ============================================================================
        await client.send_message(
            chat_id=message.chat.id,
            text=signal_message_prem,
            reply_markup=InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton("🗑 Delete This", callback_data=f"delThisPrem#{ms_id_prem}#{message.chat.id}"),
                    InlineKeyboardButton("⚙️ Update This", callback_data=f"updThisPrem#{ms_id_prem}#{message.chat.id}")
                ]]))
        await client.send_message(
            chat_id=message.chat.id,
            text=signal_message_basic,
            reply_markup=InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton("🗑 Delete This",
                                         callback_data=f"delThisBasic#{ms_id_basic}#{message.chat.id}"),
                    InlineKeyboardButton("⚙️ Update This",
                                         callback_data=f"updThisBasic#{ms_id_basic}#{message.chat.id}")
                ]]))

        index = 0
        data = {}
        while index < tp_array.size:
            key = "tp" + str(index + 1)
            price_data = {'price': str(tp_array[index])}
            premium_data = {}
            basic_data = {'tp_basic': 'no'}
            premium_tp = {'tp_premium': 'no'}
            index = index + 1
            if float(tp) >= float(index):
                premium_data['premium'] = 'yes'
            else:
                premium_data['premium'] = 'no'

            z = {**price_data, **premium_tp, **basic_data, **premium_data}
            data[key] = z
            if index == tp_array.size:
                break

        Data = {'msg_id_basic': ms_id_basic, 'msg_id_prem': ms_id_prem, 'pair': pair, 'entry': entry, 'type': type,
                'position_basic_valid': 'yes', 'position_premium_valid': 'yes',
                'takeprofits': data, 'tp': tp,
                'sl_basic': sl, 'sl_prem': sl, 'leverage': levarage, 'oscillation': s_percentage,
                'time': datetime.now()}

        collection_bot.insert_one(Data)

        log.info("databases added rows")

        time.sleep(10)

        await client.send_message(
            chat_id=Config.bot_prem_chat,
            text=signal_message_groups_bot)

        await client.send_message(
            chat_id=Config.bot_basic_chat,
            text=signal_message_groups_bot)


# ============================================================================
@client.on_message(filters.command("settings"))
async def settings(_, message):
    await message.reply_text(f"Choose what you want to change ↘️", reply_markup=InlineKeyboardMarkup(
        [[
            InlineKeyboardButton("⚙️ Delete all signals", callback_data="malll"),
            InlineKeyboardButton("➕ New Signal", callback_data="new")
        ]]))


# ============================================================================
@client.on_callback_query(filters.regex("new"))
async def new_signal(_, CallbackQuery):
    await CallbackQuery.answer(f"/newsignal : create a new signal", show_alert=True)


# ============================================================================
@client.on_callback_query(filters.regex("stop"))
async def stop_msg(_, CallbackQuery):
    await CallbackQuery.answer(f"Ok sir ", show_alert=True)
    await CallbackQuery.message.delete()


# ============================================================================
@client.on_callback_query(filters.regex("malll"))
async def del_all_messages(_, CallbackQuery):
    await client.send_message(
        chat_id=CallbackQuery.message.chat.id,
        text="Are you sure you want to clear all signals?",
        reply_markup=InlineKeyboardMarkup(
            [[
                InlineKeyboardButton("✅ Confirm", callback_data="confirm"),
                InlineKeyboardButton("❌ Cancel", callback_data="stop")
            ]]))
    await CallbackQuery.message.delete()


# ============================================================================
@client.on_callback_query(filters.regex("delThisPrem"))
async def del_message_prem(_, CallbackQuery):
    msg_id = CallbackQuery.data.split("#")[1]
    mds = collection_bot.find_one({'msg_id_prem': int(msg_id)})

    pair = mds['pair']

    url = "https://nebulous-crown-production-d964.up.railway.app/order/"  # spring
    payload = {
        "ticker": str(pair),
        "order_type": "cancelAllOrders"
    }
    print(payload)

    headers = {'Content-type': 'application/json'}
    print(headers)
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    # check if error non aggiunge segnale nei gruppi e nemmeno in mongo
    print(response.text)

    collection_bot.update_one({'msg_id_prem': int(msg_id)},
                              {'$set': {'position_premium_valid': 'no'}})

    await CallbackQuery.answer(f"✅Done , No Alerts  for this signal now", show_alert=True)
    await CallbackQuery.message.delete()


# ============================================================================
@client.on_callback_query(filters.regex("delThisBasic"))
async def del_message_basic(_, CallbackQuery):
    msg_id = CallbackQuery.data.split("#")[1]

    mds = collection_bot.find_one({'msg_id_basic': int(msg_id)})
    pair = mds['pair']

    url = "https://nebulous-crown-production-d964.up.railway.app/order/"  # spring
    payload = {
        "ticker": str(pair),
        "order_type": "cancelAllOrders"
    }
    print(payload)

    headers = {'Content-type': 'application/json'}
    print(headers)
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    # check if error non aggiunge segnale nei gruppi e nemmeno in mongo
    print(response.text)

    collection_bot.update_one({'msg_id_basic': int(msg_id)},
                              {'$set': {'position_basic_valid': 'no'}})

    await CallbackQuery.answer(f"✅Done , No Alerts  for this signal now", show_alert=True)
    await CallbackQuery.message.delete()


# ============================================================================
@client.on_callback_query(filters.regex("updThisBasic"))
async def upd_message_basic(_, CallbackQuery):
    msg_id = CallbackQuery.data.split("#")[1]
    chat_id = CallbackQuery.data.split("#")[2]
    mds = collection_bot.find_one({'msg_id_basic': int(msg_id)})

    position_basic_valid = mds['position_basic_valid']

    if position_basic_valid == 'yes':
        sl_basic = await client.ask(chat_id, f'Update SL to ?\n • for example: 1200',
                                    filters=None, timeout=60)
        sl_basic = sl_basic.text

        mds = collection_bot.find_one({'msg_id_basic': int(msg_id)})
        pair = mds['pair']

        url = "https://nebulous-crown-production-d964.up.railway.app/order/"  # spring
        payload = {
            "ticker": str(pair),
            "order_type": "updateSLOrder.basic",
            "stoploss": sl_basic
        }
        print(payload)

        headers = {'Content-type': 'application/json'}
        print(headers)
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        # check if error non aggiunge segnale nei gruppi e nemmeno in mongo
        print(response.text)

        collection_bot.update_one({'msg_id_basic': int(msg_id)},
                                  {'$set': {'sl_basic': sl_basic}})
        message = f"⚠️ Stop Loss modificato a {sl_basic}"
        await client.send_message(
            chat_id=Config.basic_chat,
            text=message,
            reply_to_message_id=int(msg_id))

    await CallbackQuery.answer(f"✅Done", show_alert=True)


# ============================================================================
@client.on_callback_query(filters.regex("updThisPrem"))
async def upd_message_prem(_, CallbackQuery):
    msg_id = CallbackQuery.data.split("#")[1]
    chat_id = CallbackQuery.data.split("#")[2]
    mds = collection_bot.find_one({'msg_id_prem': int(msg_id)})

    position_prem_valid = mds['position_premium_valid']

    if position_prem_valid == 'yes':
        sl_prem = await client.ask(chat_id, f'Update SL to ?\n • for example: 1200 (to cancel type "no")',
                                   filters=None, timeout=60)
        tp = await client.ask(chat_id, f'Update TP to ?\n • for example: 1 or 2 (to cancel type "no")',
                              filters=None, timeout=60)

        if sl_prem.text.isnumeric():
            sl_prem = sl_prem.text

            mds = collection_bot.find_one({'msg_id_prem': int(msg_id)})
            pair = mds['pair']

            url = "https://nebulous-crown-production-d964.up.railway.app/order/"  # spring

            headers = {'Content-type': 'application/json'}
            print(headers)

            if mds['type'].lower() == "long":
                payload = {
                    "ticker": str(pair),
                    "order_type": "updateTPOrder.long",
                    "stoploss": str(sl_prem)
                }
            else:
                payload = {
                    "ticker": str(pair),
                    "order_type": "updateTPOrder.short",
                    "stoploss": str(sl_prem)
                }

            response = requests.post(url, data=json.dumps(payload), headers=headers)
            # check if error non aggiunge segnale nei gruppi e nemmeno in mongo
            print(response.text)

            collection_bot.update_one({'msg_id_prem': int(msg_id)},
                                      {'$set': {'sl_prem': sl_prem}})
            message = f"⚠️ Stop Loss modificato a {sl_prem}"
            await client.send_message(
                chat_id=Config.prem_chat,
                text=message,
                reply_to_message_id=int(msg_id))
        if tp.text.isnumeric():
            tp = tp.text

            mds = collection_bot.find_one({'msg_id_prem': int(msg_id)})
            pair = mds['pair']
            entry = mds['entry']
            oscillation = mds['oscillation']

            url = "https://nebulous-crown-production-d964.up.railway.app/order/"  # spring

            headers = {'Content-type': 'application/json'}
            print(headers)

            if mds['type'].lower() == "long":
                payload = {
                    "ticker": str(pair),
                    "order_type": "updateTPOrder.long",
                    "limitt": str(entry),
                    "takeprofit": str(tp),
                    "oscillation": str(oscillation)
                }

            if mds['type'].lower() == "short":
                payload = {
                    "ticker": str(pair),
                    "order_type": "updateTPOrder.short",
                    "limitt": str(entry),
                    "takeprofit": str(tp),
                    "oscillation": str(oscillation)
                }
            print(payload)
            response = requests.post(url, data=json.dumps(payload), headers=headers)
            # check if error non aggiunge segnale nei gruppi e nemmeno in mongo
            print(response.text)

            collection_bot.update_one({'msg_id_prem': int(msg_id)},
                                      {'$set': {'tp': tp}})
            message = f"⚠️ Take Profit modificato a TP{tp}"
            await client.send_message(
                chat_id=Config.prem_chat,
                text=message,
                reply_to_message_id=int(msg_id))

    await CallbackQuery.answer(f"✅Done", show_alert=True)


# ============================================================================
@client.on_callback_query(filters.regex("confirm"))
async def del_message(_, CallbackQuery):
    try:
        collection_bot.delete_many({})
    except:
        print("Telegram says: [400 MESSAGE_EMPTY] The message is empty or no message with this ID.")


async def kk():
    print("Scheduler started")
    cursors = collection_bot.find({})

    for cursor in cursors:
        mds = collection_bot.find_one({'msg_id_basic': int(cursor['msg_id_basic'])})
        msg_id_prem = mds['msg_id_prem']
        msg_id_basic = mds['msg_id_basic']
        position_basic_valid = mds['position_basic_valid']
        position_premium_valid = mds['position_premium_valid']
        tp = mds['tp']
        entry = mds['entry']
        coin = mds['pair']
        leverage = mds['leverage']
        type = mds['type']
        sl_basic = mds['sl_basic']
        sl_prem = mds['sl_prem']
        oscillation = mds['oscillation']
        takeprofits = mds['takeprofits']
        target1 = takeprofits['tp1']
        target2 = takeprofits['tp2']
        target3 = takeprofits['tp3']
        target4 = takeprofits['tp4']
        target5 = takeprofits['tp5']
        target6 = takeprofits['tp6']
        target7 = takeprofits['tp7']
        target8 = takeprofits['tp8']
        target9 = takeprofits['tp9']
        target10 = takeprofits['tp10']

        # ============================================================================
        key = f'https://api.bybit.com/derivatives/v3/public/tickers?category=linear&symbol={coin}'
        p_data = requests.get(key)
        R_data = p_data.json()
        prc = float(R_data['result']['list'][0]['lastPrice'])

        # ============================================================================
        if position_basic_valid == 'yes' or position_premium_valid == 'yes':
            if type == "LONG":

                if prc <= float(sl_basic):

                    if position_basic_valid == 'yes':
                        if target1.get('tp_basic') == 'no':
                            message = f"❌ {coin}\nStop Loss"

                            await client.send_message(
                                chat_id=Config.basic_chat,
                                text=message,
                                reply_to_message_id=int(cursor['msg_id_basic']))
                            collection_bot.update_one({'msg_id_basic': int(msg_id_basic)},
                                                      {'$set': {'position_basic_valid': 'no'}})
                        if target1.get('tp_basic') == 'yes':
                            collection_bot.update_one({'msg_id_basic': int(msg_id_basic)},
                                                      {'$set': {'position_basic_valid': 'no'}})
                if prc <= float(sl_prem):
                    if position_premium_valid == 'yes':
                        index = 0
                        while index < 10:
                            key = "tp" + str(index + 1)
                            takeprofit = takeprofits[key]
                            if takeprofit['premium'] == 'yes' and takeprofit['tp_premium'] == 'no':

                                percentage_sl = float(
                                    (((float(entry) - float(sl_prem)) / float(sl_prem)) * 100) * float(leverage))
                                if percentage_sl >= 0:
                                    message = f"✅ {coin}\nTake profit con SL +{round(percentage_sl, 2)}%"
                                else:
                                    message = f"❌ {coin}\nStop Loss"

                                await client.send_message(
                                    chat_id=Config.prem_chat,
                                    text=message,
                                    reply_to_message_id=int(cursor['msg_id_prem']))
                                collection_bot.update_one({'msg_id_basic': int(msg_id_basic)},
                                                          {'$set': {'position_premium_valid': 'no'}})
                                break
                            index = index + 1
                            if index == 10:
                                break
                # ============================================================================

                if prc >= float(target1.get('price')):
                    message = f"✅ {coin}\n1° ON TARGET +{int(leverage) * float(oscillation) * 1}%"
                    if position_premium_valid == 'yes':
                        if target1.get('premium') == "yes" and target1.get('tp_premium') == "no":
                            await client.send_message(
                                chat_id=Config.prem_chat,
                                text=message,
                                reply_to_message_id=int(msg_id_prem))
                            collection_bot.update_one({'msg_id_basic': int(msg_id_basic)},
                                                      {'$set': {'takeprofits.tp1.tp_premium': 'yes'}})
                            if tp == '1':
                                collection_bot.update_one({'msg_id_basic': int(msg_id_basic)},
                                                          {'$set': {'position_premium_valid': 'no'}})
                    if position_basic_valid == 'yes':
                        if target1.get('tp_basic') == "no":
                            await client.send_message(
                                chat_id=Config.basic_chat,
                                text=message,
                                reply_to_message_id=int(msg_id_basic))
                            collection_bot.update_one({'msg_id_basic': int(msg_id_basic)},
                                                      {'$set': {'takeprofits.tp1.tp_basic': 'yes'}})

                # ============================================================================

                if prc >= float(target2.get('price')):
                    message = f"✅ {coin}\n2° ON TARGET +{int(leverage) * float(oscillation) * 2}%"
                    if position_premium_valid == 'yes':
                        if target2.get('premium') == "yes" and target2.get('tp_premium') == "no":
                            await client.send_message(
                                chat_id=Config.prem_chat,
                                text=message,
                                reply_to_message_id=int(msg_id_prem))
                            collection_bot.update_one({'msg_id_basic': int(msg_id_basic)},
                                                      {'$set': {'takeprofits.tp2.tp_premium': 'yes'}})
                            if tp == '2':
                                collection_bot.update_one({'msg_id_basic': int(msg_id_basic)},
                                                          {'$set': {'position_premium_valid': 'no'}})

                    if position_basic_valid == 'yes':
                        if target2.get('tp_basic') == "no":
                            await client.send_message(
                                chat_id=Config.basic_chat,
                                text=message,
                                reply_to_message_id=int(msg_id_basic))
                            collection_bot.update_one({'msg_id_basic': int(msg_id_basic)},
                                                      {'$set': {'takeprofits.tp2.tp_basic': 'yes'}})

                    # ============================================================================

                    if prc >= float(target3.get('price')):
                        message = f"✅ {coin}\n3° ON TARGET +{int(leverage) * float(oscillation) * 3}%"
                        if position_premium_valid == 'yes':
                            if target3.get('premium') == "yes" and target3.get('tp_premium') == "no":
                                await client.send_message(
                                    chat_id=Config.prem_chat,
                                    text=message,
                                    reply_to_message_id=int(msg_id_prem))
                                collection_bot.update_one({'msg_id_basic': int(msg_id_basic)},
                                                          {'$set': {'takeprofits.tp3.tp_premium': 'yes'}})
                                if tp == '3':
                                    collection_bot.update_one({'msg_id_basic': int(msg_id_basic)},
                                                              {'$set': {'position_premium_valid': 'no'}})

                        if position_basic_valid == 'yes':
                            if target3.get('tp_basic') == "no":
                                await client.send_message(
                                    chat_id=Config.basic_chat,
                                    text=message,
                                    reply_to_message_id=int(msg_id_basic))
                                collection_bot.update_one({'msg_id_basic': int(msg_id_basic)},
                                                          {'$set': {'takeprofits.tp3.tp_basic': 'yes'}})

                    # ============================================================================

                    if prc >= float(target4.get('price')):
                        message = f"✅ {coin}\n4° ON TARGET +{int(leverage) * float(oscillation) * 4}%"
                        if position_premium_valid == 'yes':
                            if target4.get('premium') == "yes" and target4.get('tp_premium') == "no":
                                await client.send_message(
                                    chat_id=Config.prem_chat,
                                    text=message,
                                    reply_to_message_id=int(msg_id_prem))
                                collection_bot.update_one({'msg_id_basic': int(msg_id_basic)},
                                                          {'$set': {'takeprofits.tp4.tp_premium': 'yes'}})
                                if tp == '4':
                                    collection_bot.update_one({'msg_id_basic': int(msg_id_basic)},
                                                              {'$set': {'position_premium_valid': 'no'}})

                        if position_basic_valid == 'yes':
                            if target4.get('tp_basic') == "no":
                                await client.send_message(
                                    chat_id=Config.basic_chat,
                                    text=message,
                                    reply_to_message_id=int(msg_id_basic))
                                collection_bot.update_one({'msg_id_basic': int(msg_id_basic)},
                                                          {'$set': {'takeprofits.tp4.tp_basic': 'yes'}})

                    # ============================================================================

                    if prc >= float(target5.get('price')):
                        message = f"✅ {coin}\n5° ON TARGET +{int(leverage) * float(oscillation) * 5}%"
                        if position_premium_valid == 'yes':
                            if target5.get('premium') == "yes" and target5.get('tp_premium') == "no":
                                await client.send_message(
                                    chat_id=Config.prem_chat,
                                    text=message,
                                    reply_to_message_id=int(msg_id_prem))
                                collection_bot.update_one({'msg_id_basic': int(msg_id_basic)},
                                                          {'$set': {'takeprofits.tp5.tp_premium': 'yes'}})
                                if tp == '5':
                                    collection_bot.update_one({'msg_id_basic': int(msg_id_basic)},
                                                              {'$set': {'position_premium_valid': 'no'}})
                        if position_basic_valid == 'yes':
                            if target5.get('tp_basic') == "no":
                                await client.send_message(
                                    chat_id=Config.basic_chat,
                                    text=message,
                                    reply_to_message_id=int(msg_id_basic))
                                collection_bot.update_one({'msg_id_basic': int(msg_id_basic)},
                                                          {'$set': {'takeprofits.tp5.tp_basic': 'yes'}})

                # ============================================================================
                if prc >= float(target6.get('price')):
                    message = f"✅ {coin}\n6° ON TARGET +{int(leverage) * float(oscillation) * 6}%"
                    if position_premium_valid == 'yes':
                        if target6.get('premium') == "yes" and target6.get('tp_premium') == "no":
                            await client.send_message(
                                chat_id=Config.prem_chat,
                                text=message,
                                reply_to_message_id=int(msg_id_prem))
                            collection_bot.update_one({'msg_id_basic': int(msg_id_basic)},
                                                      {'$set': {'takeprofits.tp6.tp_premium': 'yes'}})
                            if tp == '6':
                                collection_bot.update_one({'msg_id_basic': int(msg_id_basic)},
                                                          {'$set': {'position_premium_valid': 'no'}})
                    if position_basic_valid == 'yes':
                        if target6.get('tp_basic') == "no":
                            await client.send_message(
                                chat_id=Config.basic_chat,
                                text=message,
                                reply_to_message_id=int(msg_id_basic))
                            collection_bot.update_one({'msg_id_basic': int(msg_id_basic)},
                                                      {'$set': {'takeprofits.tp6.tp_basic': 'yes'}})

                # ============================================================================
                if prc >= float(target7.get('price')):
                    message = f"✅ {coin}\n7° ON TARGET +{int(leverage) * float(oscillation) * 7}%"
                    if position_premium_valid == 'yes':
                        if target7.get('premium') == "yes" and target7.get('tp_premium') == "no":
                            await client.send_message(
                                chat_id=Config.prem_chat,
                                text=message,
                                reply_to_message_id=int(msg_id_prem))
                            collection_bot.update_one({'msg_id_basic': int(msg_id_basic)},
                                                      {'$set': {'takeprofits.tp7.tp_premium': 'yes'}})
                            if tp == '7':
                                collection_bot.update_one({'msg_id_basic': int(msg_id_basic)},
                                                          {'$set': {'position_premium_valid': 'no'}})
                    if position_basic_valid == 'yes':
                        if target7.get('tp_basic') == "no":
                            await client.send_message(
                                chat_id=Config.basic_chat,
                                text=message,
                                reply_to_message_id=int(msg_id_basic))
                            collection_bot.update_one({'msg_id_basic': int(msg_id_basic)},
                                                      {'$set': {'takeprofits.tp7.tp_basic': 'yes'}})

                # ============================================================================
                if prc >= float(target8.get('price')):
                    message = f"✅ {coin}\n8° ON TARGET +{int(leverage) * float(oscillation) * 8}%"
                    if position_premium_valid == 'yes':
                        if target8.get('premium') == "yes" and target8.get('tp_premium') == "no":
                            await client.send_message(
                                chat_id=Config.prem_chat,
                                text=message,
                                reply_to_message_id=int(msg_id_prem))
                            collection_bot.update_one({'msg_id_basic': int(msg_id_basic)},
                                                      {'$set': {'takeprofits.tp8.tp_premium': 'yes'}})
                            if tp == '8':
                                collection_bot.update_one({'msg_id_basic': int(msg_id_basic)},
                                                          {'$set': {'position_premium_valid': 'no'}})
                    if position_basic_valid == 'yes':
                        if target8.get('tp_basic') == "no":
                            await client.send_message(
                                chat_id=Config.basic_chat,
                                text=message,
                                reply_to_message_id=int(msg_id_basic))
                            collection_bot.update_one({'msg_id_basic': int(msg_id_basic)},
                                                      {'$set': {'takeprofits.tp8.tp_basic': 'yes'}})

                # ============================================================================
                if prc >= float(target9.get('price')):
                    message = f"✅ {coin}\n9° ON TARGET +{int(leverage) * float(oscillation) * 9}%"
                    if position_premium_valid == 'yes':
                        if target9.get('premium') == "yes" and target9.get('tp_premium') == "no":
                            await client.send_message(
                                chat_id=Config.prem_chat,
                                text=message,
                                reply_to_message_id=int(msg_id_prem))
                            collection_bot.update_one({'msg_id_basic': int(msg_id_basic)},
                                                      {'$set': {'takeprofits.tp9.tp_premium': 'yes'}})
                            if tp == '9':
                                collection_bot.update_one({'msg_id_basic': int(msg_id_basic)},
                                                          {'$set': {'position_premium_valid': 'no'}})
                    if position_basic_valid == 'yes':
                        if target9.get('tp_basic') == "no":
                            await client.send_message(
                                chat_id=Config.basic_chat,
                                text=message,
                                reply_to_message_id=int(msg_id_basic))
                            collection_bot.update_one({'msg_id_basic': int(msg_id_basic)},
                                                      {'$set': {'takeprofits.tp9.tp_basic': 'yes'}})

                # ============================================================================
                if prc >= float(target10.get('price')):
                    message = f"✅ {coin}\n10° ON TARGET +{int(leverage) * float(oscillation) * 10}%"
                    if position_premium_valid == 'yes':
                        if target10.get('premium') == "yes" and target10.get('tp_premium') == "no":
                            await client.send_message(
                                chat_id=Config.prem_chat,
                                text=message,
                                reply_to_message_id=int(msg_id_prem))
                            collection_bot.update_one({'msg_id_basic': int(msg_id_basic)},
                                                      {'$set': {'takeprofits.tp10.tp_premium': 'yes'}})
                            collection_bot.update_one({'msg_id_basic': int(msg_id_basic)},
                                                      {'$set': {'position_premium_valid': 'no'}})
                    if position_basic_valid == 'yes':
                        if target10.get('tp_basic') == "no":
                            await client.send_message(
                                chat_id=Config.basic_chat,
                                text=message,
                                reply_to_message_id=int(msg_id_basic))
                            collection_bot.update_one({'msg_id_basic': int(msg_id_basic)},
                                                      {'$set': {'takeprofits.tp10.tp_basic': 'yes'}})
                            collection_bot.update_one({'msg_id_basic': int(msg_id_basic)},
                                                      {'$set': {'position_basic_valid': 'no'}})

            if type == "SHORT":
                if prc >= float(sl_basic):

                    if position_basic_valid == 'yes':
                        if target1.get('tp_basic') == 'no':
                            message = f"❌ {coin}\nStop Loss"

                            await client.send_message(
                                chat_id=Config.basic_chat,
                                text=message,
                                reply_to_message_id=int(cursor['msg_id_basic']))
                            collection_bot.update_one({'msg_id_basic': int(msg_id_basic)},
                                                      {'$set': {'position_basic_valid': 'no'}})
                        if target1.get('tp_basic') == 'yes':
                            collection_bot.update_one({'msg_id_basic': int(msg_id_basic)},
                                                          {'$set': {'position_basic_valid': 'no'}})

                if prc >= float(sl_prem):

                    if position_premium_valid == 'yes':
                        index = 0
                        while index < 10:
                            key = "tp" + str(index + 1)
                            takeprofit = takeprofits[key]
                            if takeprofit['premium'] == 'yes' and takeprofit['tp_premium'] == 'no':

                                percentage_sl = float(
                                    (((float(entry) - float(sl_prem)) / float(sl_prem)) * 100) * float(leverage))
                                if percentage_sl >= 0:
                                    message = f"✅ {coin}\nTake profit con SL +{round(percentage_sl, 2)}%"
                                else:
                                    message = f"❌ {coin}\nStop Loss"

                                await client.send_message(
                                    chat_id=Config.prem_chat,
                                    text=message,
                                    reply_to_message_id=int(cursor['msg_id_prem']))
                                collection_bot.update_one({'msg_id_basic': int(msg_id_basic)},
                                                          {'$set': {'position_premium_valid': 'no'}})
                                break
                            index = index + 1
                            if index == 10:
                                break
                # ============================================================================
                if prc <= float(target1.get('price')):
                    message = f"✅ {coin}\n1° ON TARGET +{int(leverage) * float(oscillation) * 1}%"
                    if position_premium_valid == 'yes':
                        if target1.get('premium') == "yes" and target1.get('tp_premium') == "no":
                            await client.send_message(
                                chat_id=Config.prem_chat,
                                text=message,
                                reply_to_message_id=int(msg_id_prem))
                            collection_bot.update_one({'msg_id_basic': int(msg_id_basic)},
                                                      {'$set': {'takeprofits.tp1.tp_premium': 'yes'}})
                            if tp == '1':
                                collection_bot.update_one({'msg_id_basic': int(msg_id_basic)},
                                                          {'$set': {'position_premium_valid': 'no'}})
                    if position_basic_valid == 'yes':
                        if target1.get('tp_basic') == "no":
                            await client.send_message(
                                chat_id=Config.basic_chat,
                                text=message,
                                reply_to_message_id=int(msg_id_basic))
                            collection_bot.update_one({'msg_id_basic': int(msg_id_basic)},
                                                      {'$set': {'takeprofits.tp1.tp_basic': 'yes'}})

                # ============================================================================
                if prc <= float(target2.get('price')):
                    message = f"✅ {coin}\n2° ON TARGET +{int(leverage) * float(oscillation) * 2}%"
                    if position_premium_valid == 'yes':
                        if target2.get('premium') == "yes" and target2.get('tp_premium') == "no":
                            await client.send_message(
                                chat_id=Config.prem_chat,
                                text=message,
                                reply_to_message_id=int(msg_id_prem))
                            collection_bot.update_one({'msg_id_basic': int(msg_id_basic)},
                                                      {'$set': {'takeprofits.tp2.tp_premium': 'yes'}})
                            if tp == '2':
                                collection_bot.update_one({'msg_id_basic': int(msg_id_basic)},
                                                          {'$set': {'position_premium_valid': 'no'}})
                    if position_basic_valid == 'yes':
                        if target2.get('tp_basic') == "no":
                            await client.send_message(
                                chat_id=Config.basic_chat,
                                text=message,
                                reply_to_message_id=int(msg_id_basic))
                            collection_bot.update_one({'msg_id_basic': int(msg_id_basic)},
                                                      {'$set': {'takeprofits.tp2.tp_basic': 'yes'}})

                # ============================================================================
                if prc <= float(target3.get('price')):
                    message = f"✅ {coin}\n3° ON TARGET +{int(leverage) * float(oscillation) * 3}%"
                    if position_premium_valid == 'yes':
                        if target3.get('premium') == "yes" and target3.get('tp_premium') == "no":
                            await client.send_message(
                                chat_id=Config.prem_chat,
                                text=message,
                                reply_to_message_id=int(msg_id_prem))
                            collection_bot.update_one({'msg_id_basic': int(msg_id_basic)},
                                                      {'$set': {'takeprofits.tp3.tp_premium': 'yes'}})
                            if tp == '3':
                                collection_bot.update_one({'msg_id_basic': int(msg_id_basic)},
                                                          {'$set': {'position_premium_valid': 'no'}})
                    if position_basic_valid == 'yes':
                        if target3.get('tp_basic') == "no":
                            await client.send_message(
                                chat_id=Config.basic_chat,
                                text=message,
                                reply_to_message_id=int(msg_id_basic))
                            collection_bot.update_one({'msg_id_basic': int(msg_id_basic)},
                                                      {'$set': {'takeprofits.tp3.tp_basic': 'yes'}})

                # ============================================================================
                if prc <= float(target4.get('price')):
                    message = f"✅ {coin}\n4° ON TARGET +{int(leverage) * float(oscillation) * 4}%"
                    if position_premium_valid == 'yes':
                        if target4.get('premium') == "yes" and target4.get('tp_premium') == "no":
                            await client.send_message(
                                chat_id=Config.prem_chat,
                                text=message,
                                reply_to_message_id=int(msg_id_prem))
                            collection_bot.update_one({'msg_id_basic': int(msg_id_basic)},
                                                      {'$set': {'takeprofits.tp4.tp_premium': 'yes'}})
                            if tp == '4':
                                collection_bot.update_one({'msg_id_basic': int(msg_id_basic)},
                                                          {'$set': {'position_premium_valid': 'no'}})
                    if position_basic_valid == 'yes':
                        if target4.get('tp_basic') == "no":
                            await client.send_message(
                                chat_id=Config.basic_chat,
                                text=message,
                                reply_to_message_id=int(msg_id_basic))
                            collection_bot.update_one({'msg_id_basic': int(msg_id_basic)},
                                                      {'$set': {'takeprofits.tp4.tp_basic': 'yes'}})

                # ============================================================================
                if prc <= float(target5.get('price')):
                    message = f"✅ {coin}\n5° ON TARGET +{int(leverage) * float(oscillation) * 5}%"
                    if position_premium_valid == 'yes':
                        if target5.get('premium') == "yes" and target5.get('tp_premium') == "no":
                            await client.send_message(
                                chat_id=Config.prem_chat,
                                text=message,
                                reply_to_message_id=int(msg_id_prem))
                            collection_bot.update_one({'msg_id_basic': int(msg_id_basic)},
                                                      {'$set': {'takeprofits.tp5.tp_premium': 'yes'}})
                            if tp == '5':
                                collection_bot.update_one({'msg_id_basic': int(msg_id_basic)},
                                                          {'$set': {'position_premium_valid': 'no'}})

                    if position_basic_valid == 'yes':
                        if target5.get('tp_basic') == "no":
                            await client.send_message(
                                chat_id=Config.basic_chat,
                                text=message,
                                reply_to_message_id=int(msg_id_basic))
                            collection_bot.update_one({'msg_id_basic': int(msg_id_basic)},
                                                      {'$set': {'takeprofits.tp5.tp_basic': 'yes'}})

                # ============================================================================
                if prc <= float(target6.get('price')):
                    message = f"✅ {coin}\n6° ON TARGET +{int(leverage) * float(oscillation) * 6}%"
                    if position_premium_valid == 'yes':
                        if target6.get('premium') == "yes" and target6.get('tp_premium') == "no":
                            await client.send_message(
                                chat_id=Config.prem_chat,
                                text=message,
                                reply_to_message_id=int(msg_id_prem))
                            collection_bot.update_one({'msg_id_basic': int(msg_id_basic)},
                                                      {'$set': {'takeprofits.tp6.tp_premium': 'yes'}})
                            if tp == '6':
                                collection_bot.update_one({'msg_id_basic': int(msg_id_basic)},
                                                          {'$set': {'position_premium_valid': 'no'}})
                    if position_basic_valid == 'yes':
                        if target6.get('tp_basic') == "no":
                            await client.send_message(
                                chat_id=Config.basic_chat,
                                text=message,
                                reply_to_message_id=int(msg_id_basic))
                            collection_bot.update_one({'msg_id_basic': int(msg_id_basic)},
                                                      {'$set': {'takeprofits.tp6.tp_basic': 'yes'}})

                # ============================================================================
                if prc <= float(target7.get('price')):
                    message = f"✅ {coin}\n7° ON TARGET +{int(leverage) * float(oscillation) * 7}%"
                    if position_premium_valid == 'yes':
                        if target7.get('premium') == "yes" and target7.get('tp_premium') == "no":
                            await client.send_message(
                                chat_id=Config.prem_chat,
                                text=message,
                                reply_to_message_id=int(msg_id_prem))
                            collection_bot.update_one({'msg_id_basic': int(msg_id_basic)},
                                                      {'$set': {'takeprofits.tp7.tp_premium': 'yes'}})
                            if tp == '7':
                                collection_bot.update_one({'msg_id_basic': int(msg_id_basic)},
                                                          {'$set': {'position_premium_valid': 'no'}})
                    if position_basic_valid == 'yes':
                        if target7.get('tp_basic') == "no":
                            await client.send_message(
                                chat_id=Config.basic_chat,
                                text=message,
                                reply_to_message_id=int(msg_id_basic))
                            collection_bot.update_one({'msg_id_basic': int(msg_id_basic)},
                                                      {'$set': {'takeprofits.tp7.tp_basic': 'yes'}})

                # ============================================================================
                if prc <= float(target8.get('price')):
                    message = f"✅ {coin}\n8° ON TARGET +{int(leverage) * float(oscillation) * 8}%"
                    if position_premium_valid == 'yes':
                        if target8.get('premium') == "yes" and target8.get('tp_premium') == "no":
                            await client.send_message(
                                chat_id=Config.prem_chat,
                                text=message,
                                reply_to_message_id=int(msg_id_prem))
                            collection_bot.update_one({'msg_id_basic': int(msg_id_basic)},
                                                      {'$set': {'takeprofits.tp8.tp_premium': 'yes'}})
                            if tp == '8':
                                collection_bot.update_one({'msg_id_basic': int(msg_id_basic)},
                                                          {'$set': {'position_premium_valid': 'no'}})
                    if position_basic_valid == 'yes':
                        if target8.get('tp_basic') == "no":
                            await client.send_message(
                                chat_id=Config.basic_chat,
                                text=message,
                                reply_to_message_id=int(msg_id_basic))
                            collection_bot.update_one({'msg_id_basic': int(msg_id_basic)},
                                                      {'$set': {'takeprofits.tp8.tp_basic': 'yes'}})

                # ============================================================================
                if prc <= float(target9.get('price')):
                    message = f"✅ {coin}\n9° ON TARGET +{int(leverage) * float(oscillation) * 9}%"
                    if position_premium_valid == 'yes':
                        if target9.get('premium') == "yes" and target9.get('tp_premium') == "no":
                            await client.send_message(
                                chat_id=Config.prem_chat,
                                text=message,
                                reply_to_message_id=int(msg_id_prem))
                            collection_bot.update_one({'msg_id_basic': int(msg_id_basic)},
                                                      {'$set': {'takeprofits.tp9.tp_premium': 'yes'}})
                            if tp == '9':
                                collection_bot.update_one({'msg_id_basic': int(msg_id_basic)},
                                                          {'$set': {'position_premium_valid': 'no'}})
                    if position_basic_valid == 'yes':
                        if target9.get('tp_basic') == "no":
                            await client.send_message(
                                chat_id=Config.basic_chat,
                                text=message,
                                reply_to_message_id=int(msg_id_basic))
                            collection_bot.update_one({'msg_id_basic': int(msg_id_basic)},
                                                      {'$set': {'takeprofits.tp9.tp_basic': 'yes'}})

                # ============================================================================
                if prc <= float(target10.get('price')):
                    message = f"✅ {coin}\n10° ON TARGET +{int(leverage) * float(oscillation) * 10}%"
                    if position_premium_valid == 'yes':
                        if target10.get('premium') == "yes" and target10.get('tp_premium') == "no":
                            await client.send_message(
                                chat_id=Config.prem_chat,
                                text=message,
                                reply_to_message_id=int(msg_id_prem))
                            collection_bot.update_one({'msg_id_basic': int(msg_id_basic)},
                                                      {'$set': {'takeprofits.tp10.tp_premium': 'yes'}})
                            collection_bot.update_one({'msg_id_basic': int(msg_id_basic)},
                                                      {'$set': {'position_premium_valid': 'no'}})
                    if position_basic_valid == 'yes':
                        if target10.get('tp_basic') == "no":
                            await client.send_message(
                                chat_id=Config.basic_chat,
                                text=message,
                                reply_to_message_id=int(msg_id_basic))
                            collection_bot.update_one({'msg_id_basic': int(msg_id_basic)},
                                                      {'$set': {'takeprofits.tp10.tp_basic': 'yes'}})
                            collection_bot.update_one({'msg_id_basic': int(msg_id_basic)},
                                                      {'$set': {'position_basic_valid': 'no'}})


# ==========================================
scheduler = AsyncIOScheduler()
scheduler.add_job(kk, "interval", seconds=6000)
scheduler.start()
# ==========================================

print('Bot is no online !')
client.run()
