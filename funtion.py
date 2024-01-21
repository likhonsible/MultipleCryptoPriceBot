import os
# from background import keep_alive
from datetime import datetime , timedelta
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import mplfinance as mpf
import telebot
import random
import time
from telebot import types 
import requests
import threading
import uuid
import json
from snscrape.modules import twitter as snstwi
from PIL import Image ,ImageFont,ImageDraw
from pathlib import Path
from pymongo import MongoClient
from telebot.types import ReplyKeyboardMarkup , KeyboardButton , InlineKeyboardButton , InlineKeyboardMarkup
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import csv
from io import BytesIO

bot = telebot.TeleBot("5967390922:AAEmDl-fLntXG5dFXA1IA-Yaap9-dkpMxQw")

blacklist = []

cheat = {}

API_KEY = "2748b8f5-8e99-4210-845d-78176b3a1f62"

API_KEY3 = '6FCAUJF7QR4P5Z8TNWF8XDRHRS9FMX69UR'

allowed_groups = [-648266309,-1001736231735,-1001938040524,-1001679321636,-1001856181857,-1001467085152,-1001733766092,-1001812366436]

lock = threading.Lock()

list_file = os.path.join(os.getcwd(), 'lists.json')

tweet_file = os.path.join(os.getcwd(), 'tweets.json')

try:
    with open(list_file, 'r') as f:
        persons = json.load(f)
except FileNotFoundError:
    pass

password = '1Gwhiuum22x0hmqf'
cluster_url = 'mongodb+srv://adibnslboy:' + password + '@bnslboy.02zrow4.mongodb.net/'


scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]


credentials = ServiceAccountCredentials.from_json_keyfile_name("clientgsheet.json", scope)

client2 = gspread.authorize(credentials)

spreadsheet = client2.open("Invitation data")

worksheet2 = spreadsheet.get_worksheet(2)

emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]

# Create a MongoDB client
client = MongoClient(cluster_url)

# Access the desired database
db = client['test']

giveaways = db['giveaways']

queries = db['queries']

invites = db['invites']

roles = db['roles']

dices = db['dices']

owners = db['admins']

kidz = db['users']

quizs = db['quizs']

active_quizs = {}

@bot.message_handler(commands=['start'])
def start_command(message):
    if message.text != "/start":
        return
    markup = types.InlineKeyboardMarkup()
    markup.row(
    types.InlineKeyboardButton('Join Binaryx Global ➕', url='https://t.me/binaryxGlobal')
    
)
    markup.row(
    types.InlineKeyboardButton('Get Help', url='https://telegra.ph/Binaryx-Robot-04-23'),
    types.InlineKeyboardButton('Local Groups', callback_data='local')
    
)
    markup.row(
    types.InlineKeyboardButton('💠Prices💠', callback_data='price'),
    types.InlineKeyboardButton('Games 🧩', callback_data='Games')
    )
    if message.chat.type == 'private':
        to_add_keyboard(message)
        markup.row(
        types.InlineKeyboardButton('Wallet Address 👛', callback_data='wallet_address')
    )
    first_name = message.from_user.first_name
    user_name = message.from_user.username

    bot.send_message(
        chat_id=message.chat.id,
        text=f'<a href="https://telegra.ph/file/0c7b5d3f0fee181375409.jpg">👋 </a> Hey <a href="https://t.me/{user_name}">{first_name}</a>! \nWelcome to <b>BINARYX ROBOT!</b>\n ──────────────────────────────────────────────────── \nJoin our community Now 🌐 ',
        parse_mode = 'HTML',
        reply_markup=markup
    )

def add_markup():
    markup = types.ReplyKeyboardMarkup(row_width=2,resize_keyboard=True)
    # Create buttons
    button1 = types.KeyboardButton('CNFT 💠')
    button2 = types.KeyboardButton('Match Mode 💠')
    button3 = types.KeyboardButton('Wiki 📖')
    button4 = types.KeyboardButton('AI HERO 🏆')
    button5 = types.KeyboardButton('Pancakeswap Mayor 🥞🌟')
    button6 = types.KeyboardButton('Project Matthew 🚀')
    markup.add(button1, button2, button3,button4,button5,button6)
    return markup

def add_inline_invite(chat_id,txt,y,addbutton,x,linkbutton,z,cnftbtn,a):
    markup = InlineKeyboardMarkup()
    button8 = InlineKeyboardButton(f"{addbutton}", callback_data=f"invite_add_button:{chat_id}:{x}")
    button7 = InlineKeyboardButton(f"{linkbutton}", callback_data=f"invite_link_button:{chat_id}:{z}")
    if z == "y":
        btn = InlineKeyboardButton(f"{cnftbtn}", callback_data=f"invite_cnft_button:{chat_id}:{a}")
        markup.add(btn)
    markup.add(button8,button7)
    button3 = InlineKeyboardButton(f"{txt}", callback_data=f"invite_message:{chat_id}:{y}")
    button4 = InlineKeyboardButton("Active Roles📔", callback_data=f"invite_roles:{chat_id}")
    markup.add(button3, button4)
    button5 = InlineKeyboardButton("Weekly LeaderBoard", callback_data=f"week_invite:{chat_id}")
    button6 = InlineKeyboardButton("Custom LeaderBoard", callback_data=f"custom_invite:{chat_id}")
    markup.add(button5, button6)
    button0 = InlineKeyboardButton("Export All Data 🖨", callback_data=f"export_invite:{chat_id}")
    button1 = InlineKeyboardButton("🗑 Erase All Data", callback_data=f"erase_invite:{chat_id}")
    markup.add(button0, button1)
    button2 = InlineKeyboardButton(text="🔙 Back", callback_data=f"settings:{chat_id}")
    markup.add(button2)
    return markup

def add_inline_markup2(chat_id):
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text="📜Roles" , callback_data=f"roles:{chat_id}")
    button2 = InlineKeyboardButton(text="🎉Giveaways",callback_data=f"giveaways:{chat_id}")
    button3 = InlineKeyboardButton(text="👥Invite",callback_data=f"invite:{chat_id}")
    button4 = InlineKeyboardButton(text="🎰 Dice Giveaway",callback_data=f"dice_giveaway:{chat_id}")
    markup.add(button1,button3)
    markup.add(button2,button4)
    return markup

def to_add_keyboard(message):
    markup = add_markup()
    bot.send_message(message.chat.id, '👋', reply_markup=markup)
    inline_markup = types.InlineKeyboardMarkup()
    inline_markup.row(
        types.InlineKeyboardButton('BNX , GOLD Price 💠',callback_data='price')
    )
    chek = bot.send_message(message.chat.id,".",reply_markup=inline_markup)
    bot.pin_chat_message(chek.chat.id,chek.message_id)
    bot.delete_message(chek.chat.id,chek.message_id+1)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == 'local':
        markup = types.InlineKeyboardMarkup()
        markup.row(
            types.InlineKeyboardButton('中文 中国 Chinese 🇨🇳', url='https://t.me/binaryxOfficial'),
            types.InlineKeyboardButton('हिन्दी Hindi India 🇮🇳', url='https://t.me/BinaryX_Hindi')
        )
        markup.row(
            types.InlineKeyboardButton('Brazil Português 🇧🇷', url='https://t.me/BinaryXChat'),
            types.InlineKeyboardButton('Bengali বাংলা 🇧🇩', url='https://t.me/BinaryX_Bengali')  
        )
        markup.row(
            types.InlineKeyboardButton('Arabic عربى ', url='https://t.me/BinaryX_Arabic'),
            types.InlineKeyboardButton('Turkish Türkçe ', url='https://t.me/BinaryXTurkeyOfficial')
        )
        markup.row(
            types.InlineKeyboardButton('Indonesia 🇮🇩', url='https://t.me/BinaryXIndonesia'),
            types.InlineKeyboardButton('Pakistan ', url='https://t.me/binaryxurdu')
        )
        bot.send_message(
            chat_id=call.message.chat.id,
            text="Join BinaryX local group 🌍",
            reply_markup=markup
        )
    elif call.data == 'settings':
        if call.message.chat.type == "supergroup":
            bot.answer_callback_query(call.id,"This function only be use in private.")
            return
        markup = types.InlineKeyboardMarkup()
        twinoti = "Twitter Notification"
        events = "Community Event"
        person = persons['twitter']
        person2 = persons['cnft']
        if call.from_user.id in person:
            twinoti+= "🔔"
        else:
            twinoti += "🔕"
        if call.from_user.id in person2:
            events+= "🔔"
        else:
            events += "🔕"
        markup.row(
            types.InlineKeyboardButton(f'{twinoti}',callback_data='twinoti')
        )
        markup.row(
            types.InlineKeyboardButton(f'{events}',callback_data='cnoti')
        )
        markup.row(
        types.InlineKeyboardButton('Return', callback_data='main_re'))
        bot.edit_message_text("setting open :-",call.message.chat.id,call.message.id,reply_markup=markup)
    elif call.data == 'cnoti':
        markup = types.InlineKeyboardMarkup()
        events = "Community Event"
        twinoti = "Twitter Notification"
        person = persons['twitter']
        person2 = persons['cnft']
        if call.from_user.id in person:
            twinoti+= "🔔"
        else:
            twinoti += "🔕"
        if call.from_user.id in person2:
            person2.remove(call.from_user.id)
            with open(list_file, 'w') as f:
                 json.dump(persons, f)
            events+= "🔕"
            markup.row(
            types.InlineKeyboardButton(f'{twinoti}',callback_data='twinoti')
        )
            markup.row(
            types.InlineKeyboardButton(f'{events}',callback_data='cnoti')
        )
            markup.row(
            types.InlineKeyboardButton('Return', callback_data='main_re'))
            bot.edit_message_reply_markup(call.message.chat.id,call.message.id,reply_markup=markup)
        else:
            person2.append(call.from_user.id)
            with open(list_file, 'w') as f:
                json.dump(persons, f)
            events += "🔔"
            markup.row(
            types.InlineKeyboardButton(f'{twinoti}',callback_data='twinoti')
        ) 
            markup.row(
            types.InlineKeyboardButton(f'{events}',callback_data='cnoti')
        )
            markup.row(
            types.InlineKeyboardButton('Return', callback_data='main_re'))
            bot.edit_message_reply_markup(call.message.chat.id,call.message.id,reply_markup=markup)
    elif call.data == 'twinoti':
        markup = types.InlineKeyboardMarkup()
        twinoti = "Twitter Notification"
        events = "Community Event"
        person = persons['twitter']
        person2 = persons['cnft']
        if call.from_user.id in person2:
            events+= "🔔"
        else:
            events += "🔕"
        if call.from_user.id in person:
            person.remove(call.from_user.id)
            with open(list_file, 'w') as f:
                 json.dump(persons, f)
            twinoti+= "🔕"
            markup.row(
            types.InlineKeyboardButton(f'{twinoti}',callback_data='twinoti')
        )
            markup.row(
            types.InlineKeyboardButton(f'{events}',callback_data='cnoti')
        )
            markup.row(
            types.InlineKeyboardButton('Return', callback_data='main_re'))
            bot.edit_message_reply_markup(call.message.chat.id,call.message.id,reply_markup=markup)
        else:
            person.append(call.from_user.id)
            with open(list_file, 'w') as f:
                json.dump(persons, f)
            twinoti += "🔔"
            markup.row(
            types.InlineKeyboardButton(f'{twinoti}',callback_data='twinoti')
        ) 
            markup.row(
            types.InlineKeyboardButton(f'{events}',callback_data='cnoti')
        )
            markup.row(
            types.InlineKeyboardButton('Return', callback_data='main_re'))
            bot.edit_message_reply_markup(call.message.chat.id,call.message.id,reply_markup=markup)
    elif call.data == 'price':
        symbol = "BNX"
        result = get_price(symbol)
        price, percent_change_24h = result
        response_text = f"Current Price\n<b>{symbol}</b> :<code> ${price:,.2f}</code> "
        if percent_change_24h is not None:
            change_24h_text = f"{percent_change_24h:.2f}%"
            if percent_change_24h > 0:
                response_text += f" ({change_24h_text})"
            elif percent_change_24h < 0:
                response_text += f" ({change_24h_text})"
            else:
                response_text += f" ({change_24h_text})"
        coin_id = 12082
        url = f'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?id={coin_id}'
        headers = {'X-CMC_PRO_API_KEY': API_KEY}
        response = requests.get(url, headers=headers)
        data = response.json()
        # Extract the price from the response
        price = data['data'][str(coin_id)]['quote']['USD']['price']
        percent_change_24h = data['data'][str(coin_id)]['quote']['USD']['percent_change_24h']
        response_text += f"\n<b>GOLD</b> :<code> ${price:,.5f}</code> "
        if percent_change_24h is not None:
            change_24h_text = f"{percent_change_24h:.2f}%"
            if percent_change_24h > 0:
                response_text += f" ({change_24h_text})"
            elif percent_change_24h < 0:
                response_text += f" ({change_24h_text})"
            else:
                response_text += f" ({change_24h_text})"
        bot.send_message(call.message.chat.id, response_text, parse_mode='HTML')
    elif call.data == 'wallet_address':
        user_id = call.from_user.id
        data = kidz.find_one({'user_id':user_id})
        if data:
            address = data['address']
            msg3 = bot.send_message(call.from_user.id,"This will take a min to get balance of your wallet address")
            result = get_balance(address)
            bnx_bal , gold_bal , cnft_bal = result
            bot.delete_message(msg3.chat.id, msg3.id)
            kidz.update_one({'user_id':user_id},{'$set':{'cnft_bal':cnft_bal}})
            
            all_values = worksheet2.get_all_values()
            for row_index, row in enumerate(all_values):
                if address in row:
                    if cnft_bal != row[2]:
                        worksheet2.update_cell(row_index + 1, 3, cnft_bal)
             
            data = invites.find_one({f'users.{str(call.from_user.id)}.status':"pending"})
            if data:
                user_id = data['user_id']
                chat_id = data['chat_id']
                invites.update_one({'chat_id':chat_id,'user_id':user_id},{'$inc':{'regular_count':1 ,'pending_count':-1},'$set':{f'users.{str(call.from_user.id)}.status':"done"}},upsert=True)
            bot.send_message(call.from_user.id,f"Your address {address}\n\nBNX Balance = {bnx_bal:,.2f}\nGold Balance = {gold_bal:,.2f}\nCnft = {cnft_bal}")
        else:
            markup = ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
            button1 = KeyboardButton("🚫Cancle")
            markup.add(button1)
            msg2 = bot.send_message(user_id,"Send me your Bep_20 wallet address",reply_markup=markup)
            bot.register_next_step_handler(call.message,register_wallet,msg2)
    elif call.data == 'Games':
        markup = types.InlineKeyboardMarkup()

        
        markup.row(
        types.InlineKeyboardButton('Pancakeswap Mayor 🥞🌟', callback_data='panswap')
        )
        markup.row(
        types.InlineKeyboardButton('Project Matthew 🚀', callback_data='promat'),
        types.InlineKeyboardButton('AI HERO 🏆', callback_data='aihero')
        )
        markup.row(
        types.InlineKeyboardButton('Cyber Chess', callback_data='chess'),
        types.InlineKeyboardButton('Cyber Dragon', callback_data='dragon')
        )
        markup.row(
        types.InlineKeyboardButton('Return', callback_data='main_re'))
        user_name=call.message.chat.username
        first_name = call.message.chat.first_name
        text=f'<a href="https://miro.medium.com/v2/resize:fit:828/0*_VCDMUdLT3FfZX_I">👋 </a> Hey <a href="https://t.me/{user_name}">{first_name}</a>! \nWelcome to <b>BINARYX ROBOT!</b>\n ──────────────────────────────────────────────────── \nJoin our community Now 🌐 ',

        bot.edit_message_text(text,call.message.chat.id,call.message.message_id,reply_markup=markup,parse_mode='HTML')
    elif call.data == 'main_re':
        markup = types.InlineKeyboardMarkup()
        markup.row(
        types.InlineKeyboardButton('Join Binaryx Global ➕', url='https://t.me/binaryxGlobal')

    )
        markup.row(
        types.InlineKeyboardButton('Get Help', url='https://telegra.ph/Binaryx-Robot-04-23'),
        types.InlineKeyboardButton('Local Groups', callback_data='local')

    )
        markup.row(
        types.InlineKeyboardButton('💠Prices💠', callback_data='price'),
        types.InlineKeyboardButton('Games 🧩', callback_data='Games')
        )
        markup.row(
        types.InlineKeyboardButton('Settings ⚙️', callback_data='settings')
        )
        first_name = call.message.chat.first_name
        user_name = call.message.chat.username
        text=f'<a href="https://telegra.ph/file/0c7b5d3f0fee181375409.jpg">👋 </a> Hey <a href="https://t.me/{user_name}">{first_name}</a>! \nWelcome to <b>BINARYX ROBOT!</b>\n ──────────────────────────────────────────────────── \nJoin our community Now 🌐 ',
        bot.edit_message_text(text,call.message.chat.id,call.message.message_id,reply_markup=markup,parse_mode='HTML')
    elif call.data == 'dragon':
        bot.answer_callback_query(call.id,"working on this until chill")
    elif call.data == 'chess':
        text = "<b><i>CyberChess <a href='https://i.ibb.co/5v1vW44/6o1g1ymn.png'>♟️</a>Important Links:</i></b>"

        text +="\n\nWebsite:" 
        text +="\nhttps://www.binaryx.pro/chess"

        text +="\n\nBeginners Guide: "
        text +="\nhttps://lightning-mole-a4a.notion.site/CyberChess-Wiki-8713d32de742480dae9b3432712dbfe3"

        text +="\n\nFrequently Asked Question: "
        text +="\nhttps://docs.google.com/document/d/1pQFwdPD9LOba7PmvLIuzjooqimafCdoHxmbMF_COxxs/edit?usp=sharing"

        text +="\n\n Updated Season Rewards "
        text +="\nhttps://twitter.com/binary_x/status/1575884484364247046?t=r432SVh4arZ7mSf6w93Jbw&s=19"

        text +="\n\nUpgrade Your Heroes"
        text +="\n https://t.me/binaryxGlobal/416479 "

        text +="\n\nWould like to hear more from YOU. Fill the Feedback Form below "
        text +="\n https://forms.gle/X5DL7znqk26yya2i9 "

        markup = types.InlineKeyboardMarkup()
        markup.row(
        types.InlineKeyboardButton('Return', callback_data='Games')
    )
        bot.edit_message_text(text,call.message.chat.id,call.message.message_id,reply_markup=markup,parse_mode='HTML')
    elif call.data == "promat":
        project_matthew(None , call)
    elif call.data == 'aihero':
        ai_hero(None , call)
    elif call.data == "panswap":
        pancake_swap_game(None,call)
    elif call.data.startswith(("chat:")):
        chat_id = int(call.data.split(":")[1])
        sets = roles.find({'chat_id': chat_id})
        roles_nam = []
        for set112 in sets:
            role_name = set112['roles']
            for ro in role_name:
                if ro not in roles_nam:
                    roles_nam.append(ro)
        markup = types.InlineKeyboardMarkup(row_width=2)
        for rola in roles_nam:
            callback = f"role:{rola}"
            markup.add(telebot.types.InlineKeyboardButton(rola, callback_data=callback))
    elif call.data.startswith(("role:")):
        role = call.data.split(":")[1]
    elif call.data.startswith(("nxtPage:")):
        i = int(call.data.split(":")[1])
        start = 1
        end = i + 7
        list = owners.find({'admins':call.from_user.id})
        markup = InlineKeyboardMarkup()
        is_markup = False
        if list:
            for list2 in list:
                if start <= i :
                    start += 1
                    continue
                chat = list2['chat_id']
                if 'chat_title' in list2:
                    title = list2['chat_title']
                else:
                    try:
                        details = bot.get_chat(chat)
                        title = details.title
                    except Exception:
                        continue
                button = types.InlineKeyboardButton(f"{title}",callback_data=f"chat_group:{chat}")
                markup.add(button)
                is_markup = True
                if start == end:
                    break
                start += 1
        button2 = types.InlineKeyboardButton(f"Next Page ->",callback_data=f"nxtPage:{i+7}")
        button3 = types.InlineKeyboardButton(f"<-Previous Page ",callback_data=f"nxtPage:{i-7}")
        markup.add(button3,button2)
        if is_markup:
            bot.edit_message_reply_markup(call.message.chat.id,call.message.id,reply_markup=markup)
        else:
            bot.answer_callback_query(call.id,"Not any other group found")
    elif call.data.startswith(("chat_group:")):
        chat_id = int(call.data.split(":")[1])
        chat = bot.get_chat(chat_id)
        #Please provide me the name of role 
        msg_text = f"""<b>Settings
Group: <code>{chat.title}</code></b>

<i>Select one of the settings to change.</i>"""
        markup = add_inline_markup2(chat_id)
        bot.edit_message_text(msg_text,chat_id=call.from_user.id,message_id=call.message.id,parse_mode='HTML',reply_markup=markup)
    elif call.data.startswith(("roles:")):
        chat_id = int(call.data.split(":")[1])
        markup = InlineKeyboardMarkup(row_width=2)
        button1 = InlineKeyboardButton("➕ Create New" , callback_data=f"create_role:{chat_id}")
        markup.add(button1)
        data = roles.find({'chat_id':chat_id,'role_name': {'$exists': True}})
        if data:
            for da in data:
                if 'role_name' in da:
                    count = da['count']
                    role = da['role_name']
                    button1 = InlineKeyboardButton(f"{role} [{count}]",callback_data=f"role_name:{role}:{chat_id}")
                    markup.add(button1)
        button2 = InlineKeyboardButton(text="🔙Back",callback_data=f"settings:{chat_id}")
        markup.add(button2)
        msg_text = """In this menu, you can create roles
that are available for lucky draw.

<i>You can also manage event roles from this menu.</i>"""
        bot.edit_message_text(msg_text,call.from_user.id,call.message.id,parse_mode='HTML',reply_markup=markup)
    elif call.data.startswith(("role_name:")):
        role_name = call.data.split(":")[1]
        chat_id = int(call.data.split(":")[2])
        data = roles.find({'chat_id':chat_id , 'roles':role_name})
        msg_text = f"""<b>List of users with the {role_name} role</b>\n\n"""
        if data:
            for da in data:
                user_id = da['user_id']
                name = da['first_name']
                msg_text += f"- @{name} "
        markup = InlineKeyboardMarkup()
        button = InlineKeyboardButton("➕Add User",callback_data=f"adduser:{role_name}:{chat_id}")
        button2 = InlineKeyboardButton("➖Remove User",callback_data=f"removeuser:{role_name}:{chat_id}")
        markup.add(button,button2)
        button4 = InlineKeyboardButton("✏️Edit Role",callback_data=f"edit_role:{role_name}:{chat_id}")
        button5 = InlineKeyboardButton("🗑Delete Role" , callback_data=f"del_role:{role_name}:{chat_id}")
        markup.add(button4,button5)
        msg_text += "\n\n<i>You can use the following options to add/remove users:</i>"
        button3 = InlineKeyboardButton(text="🔙Back",callback_data=f"roles:{chat_id}")
        markup.add(button3)
        bot.edit_message_text(msg_text,call.from_user.id,call.message.id,parse_mode='HTML',reply_markup=markup)
    elif call.data.startswith(("del_role:")):
        role_name = call.data.split(":")[1]
        chat_id = int(call.data.split(":")[2])
        data = roles.find_one({'chat_id':chat_id,'role_name':role_name})
        if data:
            markup = ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
            button1 = KeyboardButton("🚫Cancle")
            button2 = KeyboardButton("🗑Delete")
            markup.add(button1,button2)
            msg2 = bot.send_message(call.message.chat.id,f"Are you sure to Delete {role_name} role ?",reply_markup=markup)
            bot.register_next_step_handler(call.message,delete_role,chat_id,role_name,msg2)
        else:
            bot.answer_callback_query(call.id,f"This {role_name} does not exist anymore !!",show_alert=True,cache_time=3)
    elif call.data.startswith(("create_role:")):
            markup = ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
            button1 = KeyboardButton("🚫Cancle")
            markup.add(button1)
            chat_id = int(call.data.split(":")[1])
            msg2 = bot.send_message(call.message.chat.id,"<b>Send me role name</b> \n\n<i>must be in one word</i>",parse_mode='HTML',reply_markup=markup)
            bot.register_next_step_handler(call.message,create_role,chat_id,msg2)
    elif call.data.startswith(("edit_role:")):
        role_name = call.data.split(":")[1]
        chat_id = int(call.data.split(":")[2])
        data = roles.find_one({'chat_id':chat_id,'role_name':role_name})
        if data:
            role_count = data['count']
            msg_text = f"Role - {role_name}\nCount - {role_count}\n"
            markup = InlineKeyboardMarkup()
            if 'how_to_get' in data:
                how_to_get = data['how_to_get']
                msg_text += f"How to Get - {how_to_get}\n"
            else:
                msg_text+= f"How to Get - None\n"
            button4 = InlineKeyboardButton("✏️Edit How to get",callback_data=f"edit_how_to_get:{role_name}:{chat_id}")
            button5 = InlineKeyboardButton("✏️Change Role Name",callback_data=f"change_role_name:{role_name}:{chat_id}")
            markup.add(button4,button5)
            if "is_auto_invite" in data and data['is_auto_invite'] == True:
                auto_add = data['is_auto_invite']
                count = data['invite_count']
                msg_text += f"Auto Invite - {auto_add}\nInvite Count - {count}\n"
                
                button1 = InlineKeyboardButton("✔️ Auto Invite",callback_data=f'auto_invite_true:{role_name}:{chat_id}')   
            else:
                msg_text += f"Auto Invite - None\n"
                button1 = InlineKeyboardButton("✖️ Auto Invite",callback_data=f'auto_invite_false:{role_name}:{chat_id}')  
            if "is_auto_message" in data and data['is_auto_message'] == True:
                auto_add = data['is_auto_message']
                count = data['message_count']
                msg_text += f"Auto Message - {auto_add}\nMessage Count - {count}\n"
                button2 = InlineKeyboardButton("✔️ Auto Message",callback_data=f'auto_message_true:{role_name}:{chat_id}')
                markup.add(button1,button2)
            else:
                msg_text += f"Auto Message - None\n"
                button2 = InlineKeyboardButton("✖️ Auto Message",callback_data=f'auto_message_false:{role_name}:{chat_id}')
                markup.add(button1,button2)
            button3 = InlineKeyboardButton(text="🔙Back",callback_data=f"role_name:{role_name}:{chat_id}")
            markup.add(button3)
            bot.edit_message_text(msg_text,call.from_user.id,call.message.id,parse_mode='HTML',reply_markup=markup)
        else:
            bot.answer_callback_query(call.id,f"This {role_name} does not exist anymore !!",show_alert=True,cache_time=3)
    elif call.data.startswith(("edit_how_to_get:")):
        role_name = call.data.split(":")[1]
        chat_id = int(call.data.split(":")[2])
        data = roles.find_one({'chat_id':chat_id,'role_name':role_name})
        if data:
            markup = ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
            button1 = KeyboardButton("🚫Cancle")
            markup.add(button1)
            msg2 = bot.send_message(call.message.chat.id,"Send me description how to get this role",reply_markup=markup)
            bot.register_next_step_handler(call.message,add_how_to_get,chat_id,role_name,msg2)
        else:
            bot.answer_callback_query(call.id,"Error in finding this role ")
    elif call.data.startswith(("change_role_name:")):
        role_name = call.data.split(":")[1]
        chat_id = int(call.data.split(":")[2])
        data = roles.find_one({'chat_id':chat_id,'role_name':role_name})
        if data:
            markup = ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
            button1 = KeyboardButton("🚫Cancle")
            markup.add(button1)
            msg2 = bot.send_message(call.message.chat.id,"Send me new name for this role",reply_markup=markup)
            bot.register_next_step_handler(call.message,change_role_name,role_name,chat_id,msg2)
        else:
            bot.answer_callback_query(call.id,"Error in finding this role ")
    elif call.data.startswith(("auto_invite_true:","auto_invite_false:")):
        role_name = call.data.split(":")[1]
        chat_id = int(call.data.split(":")[2])
        data = roles.find_one({'chat_id':chat_id,'role_name':role_name})
        if data:
            if call.data.startswith(("auto_invite_true:")):
                markup = InlineKeyboardMarkup()
                button4 = InlineKeyboardButton("✏️Edit How to get",callback_data=f"edit_how_to_get:{role_name}:{chat_id}")
                button5 = InlineKeyboardButton("✏️Change Role Name",callback_data=f"change_role_name:{role_name}:{chat_id}")
                markup.add(button4,button5)
                button1 = InlineKeyboardButton("✖️ Auto Invite",callback_data=f'auto_invite_false:{role_name}:{chat_id}')
                if "is_auto_message" in data and data['is_auto_message'] == True:
                    button2 = InlineKeyboardButton("✔️ Auto Message",callback_data=f'auto_message_true:{role_name}:{chat_id}')
                    markup.add(button1,button2)
                else:
                    button2 = InlineKeyboardButton("✖️ Auto Message",callback_data=f'auto_message_false:{role_name}:{chat_id}')
                    markup.add(button1,button2)
                button3 = InlineKeyboardButton(text="🔙Back",callback_data=f"role_name:{role_name}:{chat_id}")
                markup.add(button3)
                roles.update_one({'chat_id':chat_id,'role_name':role_name},{'$set':{'is_auto_invite':False}},upsert=True)
                bot.edit_message_reply_markup(call.message.chat.id,call.message.id,reply_markup=markup)
            elif call.data.startswith(("auto_invite_false:")):
                markup = ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
                button1 = KeyboardButton("🚫Cancle")
                markup.add(button1)
                msg2 = bot.send_message(call.message.chat.id,"Send me number how many members user need to add in group to get this role",reply_markup=markup)
                bot.register_next_step_handler(call.message,auto_invite_update,chat_id,role_name,msg2)
    elif call.data.startswith(("auto_message_true:","auto_message_false:")):
        role_name = call.data.split(":")[1]
        chat_id = int(call.data.split(":")[2])
        data = roles.find_one({'chat_id': chat_id, 'role_name': role_name})

        if data:
            if call.data.startswith(("auto_message_true:")):
                markup = InlineKeyboardMarkup()
                button4 = InlineKeyboardButton("✏️Edit How to get", callback_data=f"edit_how_to_get:{role_name}:{chat_id}")
                button5 = InlineKeyboardButton("✏️Change Role Name", callback_data=f"change_role_name:{role_name}:{chat_id}")
                markup.add(button4, button5)

                if "is_auto_invite" in data and data['is_auto_invite'] == True:
                    button1 = InlineKeyboardButton("✔️ Auto Invite", callback_data=f'auto_invite_true:{role_name}:{chat_id}')
                    markup.add(button1)
                else:
                    button1 = InlineKeyboardButton("✖️ Auto Invite", callback_data=f'auto_invite_false:{role_name}:{chat_id}')
                    markup.add(button1)

                button2 = InlineKeyboardButton("✖️ Auto Message", callback_data=f'auto_message_false:{role_name}:{chat_id}')
                markup.add(button2)

                button3 = InlineKeyboardButton("🔙Back", callback_data=f"role_name:{role_name}:{chat_id}")
                markup.add(button3)

                roles.update_one({'chat_id': chat_id, 'role_name': role_name}, {'$set': {'is_auto_message': False}}, upsert=True)
                bot.edit_message_reply_markup(call.message.chat.id, call.message.id, reply_markup=markup)

            elif call.data.startswith(("auto_message_false:")):
                markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
                button1 = KeyboardButton("🚫Cancle")
                markup.add(button1)
                msg2 = bot.send_message(call.message.chat.id, "Send me the number of messages required to send to get this role", reply_markup=markup)
                bot.register_next_step_handler(msg2, auto_message_update, chat_id, role_name, msg2)
    elif call.data.startswith(("giveaways:")):
        chat_id = int(call.data.split(":")[1])
        markup = InlineKeyboardMarkup()
        button1 = InlineKeyboardButton("➕ Create New" , callback_data=f"create_giveaway:{chat_id}")
        markup.add(button1)
        data = giveaways.find({'chat_id':chat_id})
        if data:
            button2 = InlineKeyboardButton("⏳History" , callback_data=f"history_giveaway:{chat_id}")
            button3 = InlineKeyboardButton("✅Saved Data",callback_data=f"data_giveaway:{chat_id}")
            markup.add(button2,button3)
        button2 = InlineKeyboardButton(text="🔙Back",callback_data=f"settings:{chat_id}")
        markup.add(button2)
        text = """Gift Menu
Choose an option:
➕ Create New Gift - Create a new gift event.
The following buttons are not developed yet:
⏳ History - View past gift events.
✅ Saved Data - View saved gift data."""

        bot.edit_message_text(text, call.message.chat.id, call.message.id, reply_markup=markup)
    elif call.data.startswith(("create_giveaway:")):
        chat_id = call.data.split(":")[1]
        markup = ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
        button1 = KeyboardButton("🚫Cancle")
        markup.add(button1)
        msg2 = bot.send_message(call.message.chat.id,"🎉 Lottery Time 🎉\n\n🎁 Prize - ❓",reply_markup=markup)
        bot.register_next_step_handler(call.message,process_to_add,msg2,chat_id)
    elif call.data.startswith(("groleadd:")):
        title = call.data.split(":")[2]
        chat_id = int(call.data.split(":")[1])
        data = roles.find({'chat_id':chat_id})
        markup = InlineKeyboardMarkup()
        text = call.message.text
        is_role = False
        if data:
            for da in data:
                if 'role_name' in da:
                    count = da['count']
                    role = da['role_name']
                    button1 = InlineKeyboardButton(f"{role} [{count}]",callback_data=f"role_to_giveaway:{role}:{title}")
                    markup.add(button1)
                    is_role = True
            text += "\n\nChoose the role you want to add 👇"
        if is_role:
            bot.edit_message_text(text,call.message.chat.id,call.message.id,reply_markup=markup)    
        else:
            bot.answer_callback_query(call.id,"No Role Found")
    elif call.data.startswith(("role_to_giveaway:")):
        title = call.data.split(":")[2]
        role_name = call.data.split(":")[1]
        updated_results = []
        query_document = queries.find_one({'user_id':call.from_user.id})
        for result in query_document['results']:
        # If the 'title' matches, update the 'message_text' field
            if result['title'] == title:
                result['input_message_content']['message_text'] += f" {role_name}"
            updated_results.append(result)
        queries.update_one({'user_id': call.from_user.id}, {'$set': {'results': updated_results}})
        text = call.message.text
        sub = "\n\nChoose the role you want to add 👇"
        text = text[:-len(sub)]
        text += f"\n\nTo participate in this lottery, you need to have the {role_name} role."
        markup1 = InlineKeyboardMarkup()
        button1 = InlineKeyboardButton("Send Giveaway",switch_inline_query=f"{title}")
        markup1.add(button1)
        bot.edit_message_text(text,call.message.chat.id,call.message.id,reply_markup=markup1)
    elif call.data.startswith(("giveaway_how_to")):
        role_name = call.data.split(":")[1]
        chat_id = int(call.data.split(":")[2])
        data = roles.find_one({'chat_id':chat_id,'role_name':role_name})
        if data:
            if 'how_to_get' in data:
                how_to_get = data['how_to_get']
                bot.answer_callback_query(call.id,how_to_get,show_alert=True)
    elif call.data.startswith(("join_giveaway:", "leave_giveaway:","Refresh:")):
        giveaway_id = call.data.split(":")[1]
        is_how_to = False
        giveaway = giveaways.find_one({'giveaway_id':giveaway_id})
        if giveaway is None:
            bot.answer_callback_query(call.id, "Sorry, this giveaway event is no longer valid.",show_alert=True)
            return
        chat_id = call.message.chat.id
        user_id = call.from_user.id
        role = giveaway["role"]
        if role == None:
            pass
        else:
            chat_id = call.message.chat.id
            role_user = roles.find_one({'chat_id':chat_id,'user_id':user_id,'roles':role})
            if role_user is None:
                bot.answer_callback_query(call.id, f"To participate in this lottery, you must have the {role} role.",show_alert=True)
                return
        if call.data.startswith(("leave_giveaway:")):
            giveaway_id = call.data.split(":")[1]
            if user_id not in giveaway["participants"]:
                bot.answer_callback_query(call.id, "You have not yet participated in this lottery event.",show_alert=True)
                return
            current_time = time.time()
            giveaway["last_refresh_time"] = current_time
            giveaways.update_one({"giveaway_id": giveaway_id}, {"$set": {"last_refresh_time": giveaway["last_refresh_time"]}})
            giveaway["participants"].remove(user_id)
            giveaways.update_one({"giveaway_id": giveaway_id}, {"$set": {"participants": giveaway["participants"],'is_edit':True}})
            bot.answer_callback_query(call.id, "You have successfully left the lottery event.",show_alert=True)
        elif call.data.startswith(("Refresh:")):
            current_time = time.time()
            last_refresh_time = giveaway["last_refresh_time"]
            defd = current_time - last_refresh_time
            if defd < 20:
                bot.answer_callback_query(call.id, f"Please wait for {20-defd:.2f} sec before refreshing again.")
                return
            giveaway["last_refresh_time"] = current_time
            giveaways.update_one({"giveaway_id": giveaway_id}, {"$set": {"last_refresh_time": giveaway["last_refresh_time"]}})
            giveaway_id = call.data.split(":")[1]
            if user_id not in giveaway["participants"]:
                bot.answer_callback_query(call.id, "You have not joined this giveaway.",show_alert=True)
                return
            time_left = giveaway["duration"]
            join_text = f"Join"
            url = f"https://t.me/Academy_lottery_assistant_bot?start={giveaway_id}"
            leave_call = f"leave_giveaway:{giveaway_id}"
            refresh_test = f"Refresh ({time_left//86400}d:{time_left%86400//3600}h:{time_left%3600//60}m:{time_left%60}s)"
            refresh_call = f"Refresh:{giveaway_id}"
            reply_markup = telebot.types.InlineKeyboardMarkup()
            reply_markup.add(telebot.types.InlineKeyboardButton(join_text, url=url))
            reply_markup.add(telebot.types.InlineKeyboardButton("Leave", callback_data=leave_call))
            reply_markup.add(telebot.types.InlineKeyboardButton(refresh_test, callback_data=refresh_call))
            
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=reply_markup)   
    elif call.data.startswith(("history_giveaway:")):
        bot.answer_callback_query(call.id,"working on it")
        # chat_id = int(call.data.split(":")[1])
        # data = giveaways.find({'chat_id': chat_id})
        # if data:
        #     for da in data:
        #         if 'is_done' in da:
        #             giveaway_id = da['giveaway_id']
        #             amount = da[amount]
    elif call.data.startswith(("data_giveaway:")):
        bot.answer_callback_query(call.id,"working on it")
    elif call.data.startswith(("invite:")):
        chat_id = int(call.data.split(":")[1])
        bot_member = bot.get_chat_member(chat_id, 6133256899)
        if bot_member.can_invite_users is False:
            bot.answer_callback_query(call.id,"❌ Insufficient permissions for the robot, please grant at least the following admin permissions:\n- Invite members via link",show_alert=True)
            return

        msg_text = "<b>Invitation Management </b>\n<i>Members in the group use the /link to automatically generate links.\nMember can use /invites to check their invites .\nMember can use /topinvites to check top 10 of group</i>\n\n<b>Statistics</b>\n"
        data = owners.find_one({'chat_id':chat_id})
        add_count = data.get('add_count',0)
        invite_count = data.get('invite_count',0)
        num_count = data.get('user_count',0)
        
        if 'link_count' in data:
            link_count = data['link_count']
        else:
            link_count = 0
        
        msg_text += f"<i>Total number of invitations = {num_count} ({add_count} by add button , {invite_count} by invite link) </i>\n"
        msg_text += f"<i>Total number of links generated =</i> {link_count}\n\n"
        
        if 'send_msg' in data and data['send_msg'] is True:
            txt = "Send Message ✅"
            y = "y"
        else:
            txt = "Send Message ❌"
            y = "n"
        
        if 'add_msg' in data and data['add_msg'] is True:
            x_text = "Add button count ✅"
            x = "y"
        else:
            x_text = "Add button count ❌"
            x = "n"
        
        if 'link_msg' in data and data['link_msg'] is True:
            y_text = "Invite link count ✅"
            z = "y"
        else:
            y_text = "Invite link count ❌"
            z = "n"
        
        if 'cnft_msg' in data and data['cnft_msg'] is True:
            c_txt = "Need 1 CNFT in wallet ✅"
            a = "y"
        else:
            c_txt = "Need 1 CNFT in wallet ❌"
            a = "n"
        
        markup = add_inline_invite(chat_id,txt,y,x_text,x,y_text,z,c_txt,a)
        try:
            bot.edit_message_text(msg_text, call.message.chat.id, call.message.id,parse_mode='HTML',reply_markup=markup)
        except Exception:
            pass
    elif call.data.startswith(("invite_message:")):
   
        chat_id = int(call.data.split(":")[1])
        data = owners.find_one({'chat_id':chat_id})
        if 'add_msg' in data and data['add_msg'] is True:
            x_text = "Add button count ✅"
            x = "y"
        else:
            x_text = "Add button count ❌"
            x = "n"
        
        if 'link_msg' in data and data['link_msg'] is True:
            y_text = "Invite link count ✅"
            z = "y"
        else:
            y_text = "Invite link count ❌"
            z = "n"
        y = call.data.split(":")[2]
        if y == "y":
            owners.update_one({'chat_id':chat_id},{'$set':{'send_msg':False}})
            txt = "Send Message ❌"
            y = "n"
        elif y == "n":
            owners.update_one({'chat_id':chat_id},{'$set':{'send_msg':True}})
            txt = "Send Message ✅"
            y = "y"
            bot.answer_callback_query(call.id,text="When someone join via invite link \nBot send message be like -:\n\nPerson1 invites Person2",show_alert=True)
        if 'cnft_msg' in data and data['cnft_msg'] is True:
            c_txt = "Need 1 CNFT in wallet ✅"
            a = "y"
        else:
            c_txt = "Need 1 CNFT in wallet ❌"
            a = "n"
        markup = add_inline_invite(chat_id,txt,y,x_text,x,y_text,z,c_txt,a)
        try:
            bot.edit_message_reply_markup(call.message.chat.id,call.message.id,reply_markup=markup)
        except Exception:
            pass
    elif call.data.startswith(("invite_add_button:")):
        chat_id = int(call.data.split(":")[1])
        data = owners.find_one({'chat_id':chat_id})

        if 'send_msg' in data and data['send_msg'] is True:
            txt = "Send Message ✅"
            y = "y"
        else:
            txt = "Send Message ❌"
            y = "n"
        
        if 'link_msg' in data and data['link_msg'] is True:
            y_text = "Invite link count ✅"
            z = "y"
        else:
            y_text = "Invite link count ❌"
            z = "n"
        x = call.data.split(":")[2]

        if x == "y":
            owners.update_one({'chat_id':chat_id},{'$set':{'add_msg':False}})
            x_text = "Add button count ❌"
            x = "n"
        elif x == "n":
            owners.update_one({'chat_id':chat_id},{'$set':{'add_msg':True}})
            x_text = "Add button count ✅"
            x = "y"
            bot.answer_callback_query(call.id,text="When someone join via invite link \nBot send message be like -:\n\nPerson1 invites Person2",show_alert=True)
        if 'cnft_msg' in data and data['cnft_msg'] is True:
            c_txt = "Need 1 CNFT in wallet ✅"
            a = "y"
        else:
            c_txt = "Need 1 CNFT in wallet ❌"
            a = "n"
        
        markup = add_inline_invite(chat_id,txt,y,x_text,x,y_text,z,c_txt,a)
        try:
            bot.edit_message_reply_markup(call.message.chat.id,call.message.id,reply_markup=markup)
        except Exception:
            pass
    elif call.data.startswith(("invite_cnft_button:")):
        chat_id = int(call.data.split(":")[1])
        data = owners.find_one({'chat_id':chat_id})
        if 'send_msg' in data and data['send_msg'] is True:
            txt = "Send Message ✅"
            y = "y"
        else:
            txt = "Send Message ❌"
            y = "n"
        
        if 'link_msg' in data and data['link_msg'] is True:
            y_text = "Invite link count ✅"
            z = "y"
        else:
            y_text = "Invite link count ❌"
            z = "n"

        if 'add_msg' in data and data['add_msg'] is True:
            x_text = "Add button count ✅"
            x = "y"
        else:
            x_text = "Add button count ❌"
            x = "n"
        
        a = call.data.split(":")[2]

        if a == "y":
            owners.update_one({'chat_id':chat_id},{'$set':{'cnft_msg':False}})
            c_txt = "Need 1 CNFT in wallet ❌"
            a = "n"
        elif a == "n":
            owners.update_one({'chat_id':chat_id},{'$set':{'cnft_msg':True}})
            c_txt = "Need 1 CNFT in wallet ✅"
            a = "y"
            bot.answer_callback_query(call.id,text="To create link member need to have atleast 1 cnft in his wallet .\nWhen someone join via invite link that guy also need to have 1 cnft to sucessful his invite.",show_alert=True)
        markup = add_inline_invite(chat_id,txt,y,x_text,x,y_text,z,c_txt,a)
        try:
            bot.edit_message_reply_markup(call.message.chat.id,call.message.id,reply_markup=markup)
        except Exception:
            pass
    elif call.data.startswith(("invite_link_button:")):
        chat_id = int(call.data.split(":")[1])
        data = owners.find_one({'chat_id':chat_id})
        if 'add_msg' in data and data['add_msg'] is True:
            x_text = "Add button count ✅"
            x = "y"
        else:
            x_text = "Add button count ❌"
            x = "n"
        
        if 'send_msg' in data and data['send_msg'] is True:
            txt = "Send Message ✅"
            y = "y"
        else:
            txt = "Send Message ❌"
            y = "n"

        z = call.data.split(":")[2]
        if z == "y":
            owners.update_one({'chat_id':chat_id},{'$set':{'link_msg':False}})
            y_text = "Invite link count ❌"
            z = "n"
        elif z == "n":
            owners.update_one({'chat_id':chat_id},{'$set':{'link_msg':True}})
            y_text = "Invite link count ✅"
            z = "y"
            bot.answer_callback_query(call.id,text="When someone join via invite link \nBot send message be like -:\n\nPerson1 invites Person2",show_alert=True)
        if 'cnft_msg' in data and data['cnft_msg'] is True:
            c_txt = "Need 1 CNFT in wallet ✅"
            a = "y"
        else:
            c_txt = "Need 1 CNFT in wallet ❌"
            a = "n"
        markup = add_inline_invite(chat_id,txt,y,x_text,x,y_text,z,c_txt,a)
        try:
            bot.edit_message_reply_markup(call.message.chat.id,call.message.id,reply_markup=markup)
        except Exception:
            pass
    elif call.data.startswith(("invite_roles:")):
        chat_id = int(call.data.split(":")[1])
        data = roles.find({'chat_id': chat_id, 'role_name': {'$exists': True}})
        msg_txt = "Active roles || Invite count To Get\n\n"
        i = 1
        for da in data:
            if 'is_auto_invite' in da and da['is_auto_invite'] is True:
                count = da['invite_count']
                role_name = da['role_name']
                msg_txt += f"{i}. {role_name} -- {count}"
                i = i + 1
        if i == 1:
            bot.answer_callback_query(call.id,"No role found which will auto given when user invites user.",show_alert=True)
        else:
            bot.answer_callback_query(call.id,msg_txt,show_alert=True)        
    elif call.data.startswith(("week_invite:")):
        chat_id = int(call.data.split(":")[1])
        leaderboard_invite(chat_id,604800,call.from_user.id)
    elif call.data.startswith(("custom_invite:")):
        chat_id = int(call.data.split(":")[1])
        markup = ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
        button1 = KeyboardButton("🚫Cancle")
        markup.add(button1)
        bot.send_message(call.from_user.id,"Send me the time in the format of 1d,1h,1m,1s",reply_markup=markup)
        bot.register_next_step_handler(call.message,invite_time,chat_id)
    elif call.data.startswith(("export_invite:")):
        chat_id = int(call.data.split(":")[1])
        bot.answer_callback_query(call.id,"This Process may takes few seconds in collecting data from database")
        bot.send_message(call.from_user.id,"This Process may takes few seconds in collecting data from database")
        
        invi_data = owners.find_one({'chat_id':chat_id})
        if invi_data:
            link_count = invi_data.get('link_count',0)
            user_count = invi_data.get('user_count',0)
            
            data = invites.find({'chat_id': chat_id, 'first_name': {'$exists': True}}).sort('regular_count',-1)

            if data:

                selected_fields = ['first_name', 'username', 'regular_count', 'pending_count','invite_link']
                with open('invitation_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
                    csv_writer = csv.writer(csvfile)
                    csv_writer.writerow(['Total Link Count', 'Total Users Count'])
                    csv_writer.writerow([link_count, user_count])
                    csv_dict_writer = csv.DictWriter(csvfile, fieldnames=selected_fields)
                    csv_dict_writer.writeheader()
                    for row in data:
                        selected_row = {field: row.get(field, '') for field in selected_fields}
                        csv_dict_writer.writerow(selected_row)
                with open('invitation_data.csv', 'rb') as file:
                    bot.send_document(call.message.chat.id, file)
                
                data = invites.find({'chat_id': chat_id, 'first_name': {'$exists': True}}).sort('regular_count',-1)

                data2 = []
                empty_row = {'sr no.': '', 'invited_by': '', 'first_name': '', 'username': '','status':'', 'join_time': ''}
                last_invite_by = ""
                i = 1
                for daa in data:
                    if 'user' in daa:
                        for user_id, user_data in daa['users'].items():
                            
                            invited_by = daa['username']
                            if invited_by is None:
                                invited_by = daa['first_name']
                            first_name = user_data['first_name']
                            username = user_data['username']
                            join_time = user_data['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
                            status = user_data['status']
                            
                            userdata = {'sr no.':i,'invited_by': invited_by, 'first_name': first_name, 'username': username,'status':status, 'join_time': join_time}
                            data2.append(userdata)
                            i += 1
                        i = 1
                selected_fields = ['sr no.','invited_by','first_name', 'username','status', 'join_time']
                with open('invitees_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
                    csv_dict_writer = csv.DictWriter(csvfile, fieldnames=selected_fields)
                    csv_dict_writer.writeheader()
                    for row in data2:
                        if last_invite_by != row['invited_by']:
                            csv_dict_writer.writerow(empty_row)
                            last_invite_by = row['invited_by']
                        selected_row = {field: row.get(field, '') for field in selected_fields}
                        csv_dict_writer.writerow(selected_row)
                with open('invitees_data.csv', 'rb') as file:
                    bot.send_document(call.message.chat.id, file)
    elif call.data.startswith(("erase_invite:")):
        chat_id = int(call.data.split(":")[1])
        msg_text = """🚨🚨 Please note that all invitation links and invitation data will be cleared soon, the operation cannot be recovered, whether to continue:"""
        markup = InlineKeyboardMarkup()
        button1 = InlineKeyboardButton("Confim Delete All Invitation Data",callback_data=f"erase_invite1:{chat_id}")
        button2 = InlineKeyboardButton(text="🔙 Back", callback_data=f"invite:{chat_id}")
        markup.add(button1)
        markup.add(button2)
        bot.edit_message_text(msg_text,call.message.chat.id,call.message.id,reply_markup=markup)
    elif call.data.startswith(("erase_invite1:")):
        chat_id = int(call.data.split(":")[1])
        data = invites.find({'chat_id':chat_id,'invite_link':{'$exists':True}})
        for da in data:
            invite_link = da['invite_link']
            bot.revoke_chat_invite_link(chat_id,invite_link)
        invites.delete_many({'chat_id':chat_id})
        owners.update_one({'chat_id':chat_id},{'$set':{'add_count':0,'invite_count':0,'user_count':0,'link_count':0}},upsert=True)
        bot.send_message(call.from_user.id,"All Invitation Data Deleted Sucessfully")
    elif call.data.startswith(("dice_giveaway:")):
        chat_id = int(call.data.split(":")[1])
        markup = InlineKeyboardMarkup()
        button1 = InlineKeyboardButton("➕ Create New" , callback_data=f"create_dice:{chat_id}")
        markup.add(button1)
        data = dices.find({'chat_id':chat_id})
        if data:
            button2 = InlineKeyboardButton("⏳History" , callback_data=f"history_dice:{chat_id}")
            button3 = InlineKeyboardButton("✅Saved Data",callback_data=f"data_dice:{chat_id}")
            markup.add(button2,button3)
        button2 = InlineKeyboardButton(text="🔙Back",callback_data=f"settings:{chat_id}")
        markup.add(button2)
        text = """Dice Lottery Menu

Choose an option:
➕ Create New - Create a new dice event.
The following buttons are under development:
⏳ History - View past dice events.
✅ Saved Data - View saved dice data."""
        bot.edit_message_text(text, call.message.chat.id, call.message.id, reply_markup=markup)
    elif call.data.startswith(("create_dice:")):
        chat_id = int(call.data.split(":")[1])
        markup = InlineKeyboardMarkup(row_width=5)
        button1 = InlineKeyboardButton("🎲" , callback_data=f"emoji:🎲:{chat_id}")
        button2 = InlineKeyboardButton("🎯" , callback_data=f"emoji:🎯:{chat_id}")
        button3 = InlineKeyboardButton("🏀" , callback_data=f"emoji:🏀:{chat_id}")
        button4 = InlineKeyboardButton("⚽️" , callback_data=f"emoji:⚽️:{chat_id}")
        button5 = InlineKeyboardButton("🎳" , callback_data=f"emoji:🎳:{chat_id}")
        markup.add(button1,button2,button3,button4,button5)
        button6 = InlineKeyboardButton(text="🔙Back",callback_data=f"dice_giveaway:{chat_id}")
        markup.add(button6)
        text = """🎁 Dice Gift Lottery

Choose one of the following 🎲, 🎯, 🏀, ⚽️, 🎳 to create a lottery.
Set the number of times each person can participate and the end time of the lottery.
Group members can send the selected emoji to earn points.
When the lottery ends, the participant with the highest points wins."""
        bot.edit_message_text(text, call.message.chat.id, call.message.id, reply_markup=markup)
    elif call.data.startswith(("emoji:")):
        chat_id = int(call.data.split(":")[2])
        emoji = call.data.split(":")[1]
        text = f"🎉 Emoji Lucky Draw 🎉\n\n🍀 Participate in the lottery by sending the {emoji} emoji and earn points 🍀\n\n🎁 Reward - ❓"
        markup = ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
        button1 = KeyboardButton("🚫Cancle")
        markup.add(button1)
        msg2 = bot.send_message(call.message.chat.id,text,reply_markup=markup)
        bot.register_next_step_handler(call.message,dice_event_1,emoji,chat_id,msg2)
    elif call.data.startswith(("diceroleadd:")):
        title = call.data.split(":")[2]
        chat_id = int(call.data.split(":")[1])
        data = roles.find({'chat_id':chat_id})
        markup = InlineKeyboardMarkup()
        text = call.message.text
        is_role = False
        if data:
            for da in data:
                if 'role_name' in da:
                    count = da['count']
                    role = da['role_name']
                    button1 = InlineKeyboardButton(f"{role} [{count}]",callback_data=f"role_dicegiveaway:{role}:{title}")
                    markup.add(button1)
                    is_role = True
            text += "\n\nChoose the role you want to add 👇"
        if is_role:
            bot.edit_message_text(text,call.message.chat.id,call.message.id,reply_markup=markup)    
        else:
            bot.answer_callback_query(call.id,"No Role Found")
    elif call.data.startswith(("role_dicegiveaway:")):
        title = call.data.split(":")[2]
        role_name = call.data.split(":")[1]
        updated_results = []
        query_document = queries.find_one({'user_id':call.from_user.id})
        for result in query_document['results']:
        # If the 'title' matches, update the 'message_text' field
            if result['title'] == title:
                result['input_message_content']['message_text'] += f" role:{role_name}"
            updated_results.append(result)
        queries.update_one({'user_id': call.from_user.id}, {'$set': {'results': updated_results}})
        text = call.message.text
        sub = "\n\nChoose the role you want to add 👇"
        text = text[:-len(sub)]
        text += f"\n\n🌟To participate in this lucky draw, you need to have the {role_name} role"
        markup1 = InlineKeyboardMarkup()
        button1 = InlineKeyboardButton("Send Dice Giveaway",switch_inline_query=f"{title}")
        markup1.add(button1)
        bot.edit_message_text(text,call.message.chat.id,call.message.id,reply_markup=markup1)
    elif call.data.startswith(("history_dice:")):
        bot.answer_callback_query(call.id,"working on it")
        # chat_id = int(call.data.split(":")[1])
        # data = giveaways.find({'chat_id': chat_id})
        # if data:
        #     for da in data:
        #         if 'is_done' in da:
        #             giveaway_id = da['giveaway_id']
        #             amount = da[amount]
    elif call.data.startswith(("data_dice:")):
        bot.answer_callback_query(call.id,"working on it")
    elif call.data.startswith(('next_quiz:')):
        chat_id = int(call.data.split(":")[1])
        i = int(call.data.split(":")[2])
        start = 1
        markup = InlineKeyboardMarkup()
        is_change = False
        user_id = call.from_user.id
        data = quizs.find({'user_id':user_id})
        msg_txt = "Your quizs\n\n"
        for dat in data:
            if i < 0:
                break
            if start <= i :
                start += 1
                continue
            is_change = True
            quiz_id = dat['quiz_id']
            title = dat['title']
            time_left = dat.get('time_limit',"Not Set")
            questions = dat.get('questions',{})
            button = InlineKeyboardButton(title,callback_data=f"edit_quiz:{quiz_id}")
            markup.add(button)
            msg_txt += f"{start}. {title}\n❓{len(questions)} questions ▪️ ⏱ {time_left} sec\n\n"
            if start == i + 3:
                break
            start += 1
        button = InlineKeyboardButton("Next ▶️",callback_data=f"next_quiz:{chat_id}:{i+3}")
        button1 = InlineKeyboardButton("◀️ Previous",callback_data=f"next_quiz:{chat_id}:{i-3}")
        markup.add(button1,button)
        button = InlineKeyboardButton("🔙 Back",callback_data=f"settings:{chat_id}")
        markup.add(button)
        if is_change:
            bot.edit_message_text(msg_txt,call.message.chat.id,call.message.id,reply_markup=markup)
        else:
            bot.answer_callback_query(call.id,"No More quiz found **")
    elif call.data.startswith(("quiz:")):
        chat_id = int(call.data.split(":")[1])
        user_id = call.from_user.id
        data = quizs.find({'user_id':user_id})
        msg_txt = "Your quizs\n\n"
        i = 1
        markup = InlineKeyboardMarkup()
        button = InlineKeyboardButton("Create New ➕",callback_data=f"create_quiz")
        markup.add(button)
        if data:
            for dat in data:
                quiz_id = dat['quiz_id']
                title = dat['title']
                time_left = dat.get('time_limit',"Not Set")
                questions = dat.get('questions',{})
                button = InlineKeyboardButton(title,callback_data=f"edit_quiz:{quiz_id}")
                markup.add(button)
                msg_txt += f"{i}. {title}\n❓{len(questions)} questions ▪️ ⏱ {time_left} sec\n\n"
                if i == 3:
                    button = InlineKeyboardButton("Next ▶️",callback_data=f"next_quiz:{chat_id}:{i}")
                    markup.add(button)
                    break
                i = i + 1
        button = InlineKeyboardButton("🔙 Back",callback_data=f"settings:{chat_id}")
        markup.add(button)
        bot.edit_message_text(msg_txt,call.message.chat.id,call.message.id,reply_markup=markup)
    elif call.data == "create_quiz":
        create_quiz(call.message,call.from_user.id)
        bot.answer_callback_query(call.id,"Create a new quiz")
    elif call.data.startswith(("quiz_answer:")):
        try:
            chat_id = call.message.chat.id
            call_ans = call.data.split(":")[1]
            q , correct_an = active_quizs[str(chat_id)]['current_ques']
            correct_ans = correct_an['correct_option2']
            if str(call.from_user.id)in active_quizs[str(chat_id)]['joiners']:
                bot.answer_callback_query(call.id,"Your answer already submited")
                return
            data = active_quizs[str(chat_id)]
            if call_ans == correct_ans:
                time_gap = data['time_gap']
                current_time = datetime.now()
                last_time = data['last_time']
                sc = current_time - last_time
                sec1 = timedelta(seconds=1)
                sco = 500 + time_gap - int(sc/sec1)
                if 'users' in data:
                    if str(call.from_user.id) in data['users'].keys():
                        score = data['users'][str(call.from_user.id)]['score']
                        data['users'][str(call.from_user.id)]['score'] = score + sco
                    else:
                        data['users'][str(call.from_user.id)] = {'score':sco,'username':call.from_user.username,'first_name':call.from_user.first_name}
                else :
                    active_quizs[str(chat_id)]['users'] = {}
                    data['users'][str(call.from_user.id)] = {'score': sco ,'username':call.from_user.username,'first_name':call.from_user.first_name}
            bot.answer_callback_query(call.id,"Answer sucessfully submited ")
            active_quizs[str(chat_id)]['joiners'].append(str(call.from_user.id))
        except Exception as e:
            print(e)
            bot.answer_callback_query(call.id,'Intreaction Failed')
            pass
    elif call.data == "ended":
        bot.answer_callback_query(call.id,"This quiz question already ended. ")
    elif call.data.startswith(("edit_quiz:")):
        quiz_id = call.data.split(":")[1]
        data = quizs.find_one({'quiz_id':quiz_id})
        if data:
            markup = InlineKeyboardMarkup()
            quiz_id = data['quiz_id']
            title = data['title']
            time_left = data.get('time_limit',"Not Set")
            questions = data.get('questions',{})
            button = InlineKeyboardButton("Add More Questions",callback_data=f"add_quiz:{quiz_id}")
            button1 = InlineKeyboardButton("Edit Question",callback_data=f"edit_ques:{quiz_id}")
            button2 = InlineKeyboardButton("Delete",callback_data=f"delete_quiz:{quiz_id}")
            button3 = InlineKeyboardButton("Edit time limit",callback_data=f"time_quiz:{quiz_id}")
            button4 = InlineKeyboardButton('Share quiz',switch_inline_query=f"{title}")
            markup.add(button,button1)
            markup.add(button2,button3)
            markup.add(button4)
            msg_txt = f"{title}\n❓{len(questions)} questions ▪️ ⏱ {time_left} sec"
            bot.edit_message_text(msg_txt,call.message.chat.id,call.message.id,reply_markup=markup)
        else:
            bot.answer_callback_query(call.id,"Quiz Not Found")
    elif call.data.startswith(("add_quiz:")):
        quiz_id = call.data.split(":")[1]
        data = quizs.find_one({'quiz_id':quiz_id})
        if data:
            bot.answer_callback_query(call.id,"Send me a question")
            markup = ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
            button1 = KeyboardButton("🚫Cancle")
            button2 = KeyboardButton("Create a question",request_poll=telebot.types.KeyboardButtonPollType(type="quiz"))
            markup.add(button2,button1)
            msg2 = bot.send_message(call.from_user.id,"Send Me a question ",reply_markup=markup)
            bot.register_next_step_handler(call.message,create_quiz3,msg2,quiz_id)
    elif call.data.startswith(("edit_ques:")):
        bot.answer_callback_query(call.id,"working on it")
    elif call.data.startswith(("delete_quiz:")):
        quiz_id = call.data.split(":")[1]
        data = quizs.find_one({'quiz_id':quiz_id})
        if data:
            markup = InlineKeyboardMarkup()
            btn = InlineKeyboardButton("Delete Quiz",callback_data=f"del_quiz:{quiz_id}")
            btn2 = InlineKeyboardButton("Delete a Question",callback_data=f"del_ques:{quiz_id}")
            markup.add(btn)
            markup.add(btn2)
            button = InlineKeyboardButton("🔙 Back",callback_data=f"edit_quiz:{quiz_id}")
            markup.add(button)
            bot.edit_message_reply_markup(call.message.chat.id,call.message.id,reply_markup=markup)
        else:
            bot.answer_callback_query(call.id,"Quiz Not Found")
    elif call.data.startswith(("del_ques:")):
        bot.answer_callback_query(call.id,"Working on it")
    elif call.data.startswith(("del_quiz:")):
        quiz_id = call.data.split(":")[1]
        data = quizs.find_one({'quiz_id':quiz_id})
        if data:
            quizs.delete_one({'quiz_id':quiz_id})
            bot.edit_message_text("Quiz Deleted !!!",call.message.chat.id,call.message.id)
        else:
            bot.answer_callback_query(call.id,"Quiz Not Found")
    elif call.data.startswith(("time_quiz:")):
        quiz_id = call.data.split(":")[1]
        data = quizs.find_one({'quiz_id':quiz_id})
        if data:
            markup = quiz_time_keyboard()
            bot.send_message(call.message.chat.id,"Please set a time limit for questions. In groups, the bot will send the next question as soon as this time is up.\n\nWe recommend using longer timers only if your quiz involves complex problems (like math, etc.). For most trivia-like quizzes, 10-30 seconds are more than enough.\n\nLike 10s,20s,30s make sure that time will be round off 10s",reply_markup=markup)
            bot.register_next_step_handler(call.message,quiz_time,quiz_id)
        else:
            bot.answer_callback_query(call.id,"Quiz not found")

def quiz_time(message,quiz_id):
    duration = message.text
    try:
        duration = int(duration[:-1]) * {"d": 86400, "h": 3600, "m": 60, "s": 1}[duration[-1]]
    except Exception as e:
        try:
            bot.delete_message(message.chat.id, message.id)
        except Exception:
            pass
        bot.send_message(message.chat.id,"Error : Time limit should be in the format 1d, 1h, 1m, or 1s.")
        bot.register_next_step_handler(message,quiz_time,quiz_id)
        return
    data = quizs.find_one({'quiz_id':quiz_id})
    if data:
        markup = types.ReplyKeyboardRemove()
        quizs.update_one({'quiz_id':quiz_id},{'$set':{'time_limit':duration}})
        bot.send_message(message.chat.id,f"New time limit is set to {duration} second .",reply_markup=markup)

def quiz_time_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True,row_width=3)
    button1 = KeyboardButton("10s")
    button2 = KeyboardButton("20s")
    button3 = KeyboardButton("30s")
    button4 = KeyboardButton("1m")
    button5 = KeyboardButton("2m")
    button6 = KeyboardButton("3m")
    button7 = KeyboardButton("5m")
    button8 = KeyboardButton("10m")
    button9 = KeyboardButton("30m")
    markup.add(button1,button2,button3)
    markup.add(button4,button5,button6)
    markup.add(button7,button8,button9)
    return markup

def create_quiz(message,user_id):
    markup = ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
    button1 = KeyboardButton("🚫Cancle")
    markup.add(button1)
    msg2 = bot.send_message(user_id,"Send me the title of your quiz (e.g., ‘Quiz 1’)",reply_markup=markup)
    bot.register_next_step_handler(message,create_quiz2,user_id,msg2)

def create_quiz2(message,user_id,msg2):
    markup = ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
    button1 = KeyboardButton("🚫Cancle")
    button2 = KeyboardButton("Create a question",request_poll=telebot.types.KeyboardButtonPollType(type="quiz"))
    markup.add(button2,button1)
    if message.text == "🚫Cancle":
        try:
            bot.delete_message(msg2.chat.id, msg2.id)
            bot.delete_message(message.chat.id, message.id)
            return
        except Exception:
            pass
    quiz_id = str((uuid.uuid4()))
    document = {
        'user_id':message.from_user.id,
        'quiz_id':quiz_id,
        'title':message.text,
        'questions':{}
    }
    quizs.insert_one(document)
    try:
        bot.delete_message(msg2.chat.id, msg2.id)
    except Exception:
        pass
    msg2 = bot.send_message(user_id,"Send Me a question ",reply_markup=markup)
    bot.register_next_step_handler(message,create_quiz3,msg2,quiz_id)

def create_quiz3(message,msg2,quiz_id):
    markup = ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
    button1 = KeyboardButton("☑️Done")
    button2 = KeyboardButton("Create a question",request_poll=telebot.types.KeyboardButtonPollType(type="quiz"))
    markup.add(button2,button1)
    if message.text == "🚫Cancle":
        bot.delete_message(msg2.chat.id, msg2.id)
        bot.delete_message(message.chat.id, message.id)
        return
    elif message.text == "☑️Done":
        markup = quiz_time_keyboard()
        try:
            bot.delete_message(msg2.chat.id, msg2.id)
            bot.delete_message(message.chat.id, message.id)
        except Exception:
            pass
        msg2 = bot.send_message(message.chat.id,"Please set a time limit for questions. In groups, the bot will send the next question as soon as this time is up.\n\nWe recommend using longer timers only if your quiz involves complex problems (like math, etc.). For most trivia-like quizzes, 10-30 seconds are more than enough.\n\nLike 10s,20s,30s make sure that time will be round off 10s",reply_markup=markup)
        bot.register_next_step_handler(message,create_quiz4,msg2,quiz_id)
        return
    if message.content_type == 'poll':
        data = quizs.find_one({'quiz_id':quiz_id})
        if data:
            try:
                bot.delete_message(msg2.chat.id, msg2.id)
            except Exception:
                pass

            question = message.poll.question
            options = []
            for option in message.poll.options:
                options.append(option.text)
            correct_index = message.poll.correct_option_id
            correct_answer = options[correct_index]
            daa = data['questions']
            title = data['title']
            daa[question] = {'options':options,'correct_option':correct_answer}
            msg2 = bot.send_message(message.chat.id,f"Now your quiz '{title}' have {len(daa)} questions.\n\nNow send the next question\n\nWhen done, simply send ☑️Done to finish creating the quiz.",reply_markup=markup)
            quizs.update_one({'quiz_id':quiz_id},{'$set':{'questions':daa}})
            bot.register_next_step_handler(message,create_quiz3,msg2,quiz_id)
            return
    else:
        bot.send_message(message.chat.id,"Please send a question . Using create a option button")
        bot.register_next_step_handler(message,create_quiz3,msg2,quiz_id)

def create_quiz4(message,msg2,quiz_id):
    duration = message.text
    try:
        duration = int(duration[:-1]) * {"d": 86400, "h": 3600, "m": 60, "s": 1}[duration[-1]]
    except Exception as e:
        try:
            bot.delete_message(message.chat.id, message.id)
        except Exception:
            pass
        bot.send_message(message.chat.id,"Error : Time limit should be in the format 1d, 1h, 1m, or 1s.")
        bot.register_next_step_handler(message,create_quiz4,msg2,quiz_id)
        return
    data = quizs.find_one({'quiz_id':quiz_id})
    if data:
        title = data['title']
        quizs.update_one({'quiz_id':quiz_id},{'$set':{'time_limit':duration}})
        markup = InlineKeyboardMarkup()
        button = InlineKeyboardButton("Share quiz in Group",url=f"https://t.me/Tic4techgamebot?startgroup=quiz:{quiz_id}")
        button1 = InlineKeyboardButton('Share quiz',switch_inline_query=f"{title}")
        markup.add(button1)
        markup.add(button)
        id = str((uuid.uuid4()))
        result = {
            "id": id,
            "title": title,
            "input_message_content": {
                "message_text": f"/quies {quiz_id}"
            }
        }
        queries.update_one(
            {'user_id': message.from_user.id},
            {'$addToSet': {'results': result}},
            upsert=True
        )
        ques = data['questions']
        markup2 = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id,"👍 Quiz created.",reply_markup=markup2)
        bot.send_message(message.chat.id,f"<b>{title}</b>\n❓{len(ques)} ▪️ ⏱ {duration} sec",reply_markup=markup,parse_mode='HTML')

def time_check2():
    with lock:
        time.sleep(10)
        while True:
            i= 1
            try:
                for chat_id , data in active_quizs.items():
                    current_time = datetime.now()
                    last_time = data['last_time']
                    time_gap = timedelta(seconds=data['time_gap'])
                    i = i + 1
                    if last_time + time_gap <= current_time:
                        ques = data['questions']
                        if data['edit_msg']:
                            msg_id = data['msg_id']
                            markup = InlineKeyboardMarkup()
                            button = InlineKeyboardButton("Ended",callback_data="ended")
                            markup.add(button)
                            bot.edit_message_reply_markup(chat_id,msg_id,reply_markup=markup)
                            data['edit_msg'] = False
                            ques2 = data['current_ques']
                            que , data4 = ques2
                            correct_answer2 = data4['correct_option']
                            bot.send_message(chat_id,f"<b>{que}</b>\nTime's up!\n\ncorrect ans - {correct_answer2}",parse_mode='HTML')
                        if data['send_leader']:
                            if 'users' in data:
                                msg_txt = "<b>Leaderboard</b>\n\n"
                                sorted_participant = sorted(data["users"].items(), key=lambda x: x[1]['score'], reverse=True)
                                if int(data['total_ques']) == (int(data['done_ques'])-1):
                                    msg_txt = "<b>Final Leaderboard</b>\n\n"
                                    end = 20
                                    for j, (user_id, data3) in enumerate(sorted_participant,start=1):
                                        if j == end:
                                            end = end + 20
                                            bot.send_message(chat_id,msg_txt,parse_mode='HTML')
                                            msg_txt = "----------------\n"
                                        username = data3['username']
                                        if username is None:
                                            username = data3['first_name']
                                        score = data3['score']
                                        msg_txt += f"#{j}. {username} - {score}\n"
                                    bot.send_message(chat_id,msg_txt,parse_mode='HTML')
                                else:
                                    for j, (user_id, data3) in enumerate(sorted_participant,start=1):
                                        if j > 10:
                                            break
                                        username = data3['username']
                                        if username is None:
                                            username = data3['first_name']
                                        score = data3['score']
                                        msg_txt += f"#{j}. {username} - {score}\n"
                                    bot.send_message(chat_id,msg_txt,parse_mode='HTML')
                                    pass
                            else:
                                bot.send_message(chat_id,"No one participate yet\n\nQuiz will continue in 10 sec")
                            data['send_leader'] = False
                            continue
                        data['last_time'] = current_time
                        if len(ques) == 0:
                            del active_quizs[str(chat_id)]
                            continue
                        for q ,data2 in ques.items():
                            correct_answer = data2['correct_option']
                            total = data['total_ques']
                            if 'done_ques' in data:
                                done = data['done_ques']
                            else:
                                done = 1
                            data['current_ques'] = q , data2
                            del active_quizs[str(chat_id)]['questions'][q]
                            msg_text = f"<b>[{done}/{total}] {q} </b>\n\n"
                            active_quizs[str(chat_id)]['done_ques'] = done + 1
                            buttons = []
                            but = []
                            for start , option in enumerate(data2['options'],start=1):
                                if start == 6:
                                    buttons.append(but)
                                    but = []
                                emoji = emojis[start - 1]
                                msg_text += f"{emoji} {option}\n"
                                if correct_answer == option:
                                    data2['correct_option2'] = str(start)
                                button1 = InlineKeyboardButton(f"{emoji}",callback_data=f"quiz_answer:{start}")
                                but.append(button1)
                            buttons.append(but)
                            markup = InlineKeyboardMarkup(buttons,row_width=5) 
                            msg = bot.send_message(chat_id,msg_text,reply_markup=markup,parse_mode='HTML')
                            data['edit_msg'] = True
                            data['send_leader'] = True
                            data['msg_id'] = msg.id
                            active_quizs[str(chat_id)]['joiners'] = []
                            break
            except Exception as e:      
                time_thread = threading.Thread(target=time_check2)
                time_thread.start()
                print(e)
                pass
            if i == 1:
                return False
            time.sleep(10)

def start_quiz(quiz_id,chat_id,msg_id):
    
    data = quizs.find_one({'quiz_id':quiz_id})
    if data:
        questions = data['questions']
        time_gap = data['time_limit']
        current_time = datetime.now() - timedelta(seconds=time_gap)
        length = len(questions)
        active_quizs[str(chat_id)] = {'questions':questions,'time_gap':time_gap,'last_time':current_time,'quiz_id':quiz_id,'total_ques':length,
                                      'edit_msg':False,'send_leader':False}
        msg_text = f"🏁 Get Ready For Quiz '{data['title']}'\n\n❓{len(questions)} questions\n⏱{time_gap} seconds per question."
        msg_text+=f"\n🔹A correct answer awards 500-{500 + time_gap} points."
        bot.send_message(chat_id,msg_text)
        try:
            if msg_id:
                bot.delete_message(chat_id,msg_id)
        except Exception:
            pass
        time_thread = threading.Thread(target=time_check2)
        time_thread.start()
    else:
        bot.send_message(chat_id,"Quiz not found")

def register_wallet(message,msg2):
    markup = add_markup()
    if message.text == "🚫Cancle":
        bot.delete_message(msg2.chat.id, msg2.id)
        bot.delete_message(message.chat.id, message.id)
        return
    if message.text.startswith(("0x")):
        address = message.text
        data = kidz.find_one({'address':address})
        if data:
            bot.delete_message(msg2.chat.id, msg2.id)
            bot.delete_message(message.chat.id, message.id)
            bot.send_message(message.chat.id,"This address already register",reply_markup=markup)
            return
        kidz.update_one({'user_id':message.from_user.id},{'$set':{'address':address}},upsert=True)
        msg3 = bot.send_message(message.from_user.id,f"Your address has been saved\n{address}\n\n")
        result = get_balance(address)
        bnx_bal , gold_bal , cnft_bal = result
        bot.delete_message(msg3.chat.id, msg3.id)
        bot.delete_message(msg2.chat.id, msg2.id)
        bot.delete_message(message.chat.id, message.id)
        kidz.update_one({'user_id':message.from_user.id},{'$set':{'cnft_bal':cnft_bal}})
        rows = []
        username = message.from_user.username
        if username is None:
            username = message.from_user.first_name
        all_values = worksheet2.get_all_values()
        rows.append([username,address,cnft_bal])
        existing_row_count = len(all_values)
        worksheet2.insert_rows(rows, existing_row_count + 1) 
        if cnft_bal >= 1:
            data = invites.find_one({f'users.{str(message.from_user.id)}.status':"pending"})
            if data:
                user_id = data['user_id']
                chat_id = data['chat_id']
                invites.update_one({'chat_id':chat_id,'user_id':user_id},{'$inc':{'regular_count':1 ,'pending_count':-1},'$set':{f'users.{str(message.from_user.id)}.status':"done"}},upsert=True)
        bot.send_message(message.from_user.id,f"Your address has been saved\n{address}\n\nBNX Balance = {bnx_bal:,.2f}\nGold Balance = {gold_bal:,.2f}\nCnft = {cnft_bal}",reply_markup=markup)
    else:
        bot.send_message(message.from_user.id,"Wrong address .",reply_markup=markup)

def get_balance(address):
    gold_add = "0xb3a6381070b1a15169dea646166ec0699fdaea79"
    bnx_add = "0x5b1f874d0b0C5ee17a495CbB70AB8bf64107A3BD"
    cnft_add = "0xA7b842FE0D55302a3C153AFC821fb81d56D48B0a"

    def get_token_balance(contract_address):
        url = f'https://api.bscscan.com/api?module=account&action=tokenbalance&contractaddress={contract_address}&address={address}&tag=latest&apikey={API_KEY3}'
        response = requests.get(url).json()
        return int(response['result']) / 10**18

    def get_cnft_balance():
        cnft_bal = 0
        page = 1
        while True:
            url = f'https://api.bscscan.com/api?module=account&action=tokennfttx&contractaddress={cnft_add}&address={address}&page={page}&offset=100&startblock=0&endblock=999999999&sort=asc&apikey={API_KEY3}'
            response = requests.get(url).json()
            txs = response.get('result', [])
            if not txs:
                break
            cnft_bal += len(txs)
            page += 1
        return cnft_bal

    try:
        gold_bal = get_token_balance(gold_add)
    except:
        gold_bal = 0
    try:
        bnx_bal = get_token_balance(bnx_add)
    except:
        bnx_bal = 0
    try:
        cnft_bal = get_cnft_balance()
    except:
        cnft_bal = 0

    return bnx_bal, gold_bal, cnft_bal

def dice_event_1(message,emoji,chat_id,msg2):
    markup = ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
    button1 = KeyboardButton("🚫Cancle")
    markup.add(button1)
    if message.text == "🚫Cancle":
        bot.delete_message(msg2.chat.id, msg2.id)
        bot.delete_message(message.chat.id, message.id)
        return
    reward = message.text
    bot.delete_message(msg2.chat.id, msg2.id)
    msg2 = bot.send_message(message.chat.id,f"🎉 Emoji Lucky Draw 🎉\n\n🍀 Participate in the lottery by sending the {emoji} emoji and earn points 🍀\n\n🎁 Reward - {reward} \n\n🏆 Chances - ❓ 🌟",reply_markup=markup)
    bot.register_next_step_handler(message,dice_event_2,emoji,chat_id,reward,msg2)

def dice_event_2(message,emoji,chat_id,reward,msg2):
    markup = ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
    button1 = KeyboardButton("🚫Cancle")
    markup.add(button1)
    if message.text == "🚫Cancle":
            bot.delete_message(msg2.chat.id, msg2.id)
            bot.delete_message(message.chat.id, message.id)
            return
    try:
        chances = int(message.text)
    except Exception:
        bot.delete_message(msg2.chat.id, msg2.id)
        bot.send_message(message.chat.id,"Send me no. of chances like 3,5,7",reply_markup=markup)
        bot.register_next_step_handler(message,dice_event_2,emoji,chat_id,reward,msg2)
        return
    bot.delete_message(msg2.chat.id, msg2.id)
    msg2 = bot.send_message(message.chat.id,f"🎉 Emoji Lucky Draw 🎉\n\n🍀 Participate in the lottery by sending the {emoji} emoji and earn points 🍀\n\n🎁 Reward - {reward} \n\n🏆 Chances - {chances} 🌟\n\n⏰ Ends in - ❓ 🔥",reply_markup=markup)
    bot.register_next_step_handler(message,dice_event_3,emoji,chat_id,reward,chances,msg2)

def dice_event_3(message,emoji,chat_id,reward,chances,msg2):
    markup = ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
    button1 = KeyboardButton("🚫Cancle")
    markup.add(button1)
    if message.text == "🚫Cancle":
            bot.delete_message(msg2.chat.id, msg2.id)
            bot.delete_message(message.chat.id, message.id)
            return
    duration = message.text
    try:
        duration = int(duration[:-1]) * {"d": 86400, "h": 3600, "m": 60, "s": 1}[duration[-1]]
    except Exception as e:
        bot.delete_message(message.chat.id, message.id)
        bot.send_message(message.chat.id,"Error : Duration should be in the format 1d, 1h, 1m, or 1s.",reply_markup=markup)
        bot.register_next_step_handler(message,dice_event_3,emoji,chat_id,reward,chances,msg2)
        return
    time_left = duration
    time_left_str = f"{time_left // 86400}d:{(time_left % 86400) // 3600}h:{(time_left % 3600) // 60}m:{time_left % 60}s"
    id = str(uuid.uuid4())
    reward = reward.replace(" ", "_")
    message_text = f"/dices {emoji} {chances} {reward} {duration}s"
    title = str(uuid.uuid4())
    result = {
            "id": id,
            "title": title,
            "input_message_content": {
                "message_text": message_text
            }
        }
    queries.update_one(
            {'user_id': message.from_user.id},
            {'$addToSet': {'results': result}},
            upsert=True
        )
    markup1= InlineKeyboardMarkup()
    bot.delete_message(msg2.chat.id, msg2.id)
    button1 = InlineKeyboardButton("Send Dice Giveaway",switch_inline_query=f"{title}")
    markup1.add(button1)
    button2 = InlineKeyboardButton("Add Role Required",callback_data=f"diceroleadd:{chat_id}:{title}")
    markup1.add(button2)
    bot.send_message(message.chat.id,f"🎉 Emoji Lucky Draw 🎉\n\n🍀 Participate in the lottery by sending the {emoji} emoji and earn points 🍀\n\n🎁 Reward - {reward} \n\n🏆 Chances - {chances} 🌟\n\n⏰ Ends in - {time_left_str} 🔥\n\n🎊 Achieve a high score & win big prizes! 🎁" , reply_markup=markup1)

def process_to_add(message,msg2,chat_id):
    markup = ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
    button1 = KeyboardButton("🚫Cancle")
    markup.add(button1)
    if message.text == "🚫Cancle":
            bot.delete_message(msg2.chat.id, msg2.id)
            bot.delete_message(message.chat.id, message.id)
            return
    reward = message.text
    bot.delete_message(msg2.chat.id, msg2.id)
    msg2 = bot.send_message(message.chat.id,f"🎉 Lottery Time 🎉\n\n🎁 Prize -  {reward}\n\n🏆 Number of Winners - ❓",reply_markup=markup)
    bot.register_next_step_handler(message,process_to_add_2 , msg2,chat_id,reward)

def process_to_add_2(message ,msg2,chat_id,reward):
    markup = ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
    button1 = KeyboardButton("🚫Cancle")
    markup.add(button1)
    if message.text == "🚫Cancle":
            bot.delete_message(msg2.chat.id, msg2.id)
            bot.delete_message(message.chat.id, message.id)
            return
    num_winners = message.text
    bot.delete_message(msg2.chat.id, msg2.id)
    msg2 = bot.send_message(message.chat.id,f"🎉 Lottery Time 🎉\n\n🎁 Prize -  {reward}\n\n🏆 Number of Winners - {num_winners}\n\n⏱ Ends in - ❓",reply_markup=markup)

    bot.register_next_step_handler(message , process_to_add_3 , msg2 ,chat_id,reward, num_winners)

def process_to_add_3(message,msg2 ,chat_id,reward, num_winners):
    markup = ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
    button1 = KeyboardButton("🚫Cancle")
    markup.add(button1)
    if message.text == "🚫Cancle":
            bot.delete_message(msg2.chat.id, msg2.id)
            bot.delete_message(message.chat.id, message.id)
            return
    duration = message.text
    try:
        duration = int(duration[:-1]) * {"d": 86400, "h": 3600, "m": 60, "s": 1}[duration[-1]]
    except Exception as e:
        bot.delete_message(message.chat.id, message.id)
        bot.send_message(message.chat.id,"Error : Duration should be in the format 1d, 1h, 1m, or 1s.",reply_markup=markup)
        bot.register_next_step_handler(message , process_to_add_3 , msg2 ,chat_id,reward, num_winners)
        return
    
    time_left = duration
    time_left_str = f"{time_left // 86400}d:{(time_left % 86400) // 3600}h:{(time_left % 3600) // 60}m:{time_left % 60}s"
    id = str(uuid.uuid4())
    description = f"Giveaway of {reward} in {num_winners} winners \n which ends in {time_left_str} duration"
    reward = reward.replace(" ", "_")
    message_text = f"/giveaway {reward} {num_winners} {duration}s"
    title = str(uuid.uuid4())
    result = {
            "id": id,
            "title": title,
            "description":description,
            "input_message_content": {
                "message_text": message_text
            }
        }
    queries.update_one(
            {'user_id': message.from_user.id},
            {'$addToSet': {'results': result}},
            upsert=True
        )
    # bot.edit_message_reply_markup(message.chat.id,msg2.id,reply_markup=markup)
    markup1= InlineKeyboardMarkup()
    bot.delete_message(msg2.chat.id, msg2.id)
    button1 = InlineKeyboardButton("Send Giveaway",switch_inline_query=f"{title}")
    markup1.add(button1)
    button2 = InlineKeyboardButton("Add Role Required",callback_data=f"groleadd:{chat_id}:{title}")
    markup1.add(button2)
    bot.send_message(message.chat.id,f"🎉 Lottery Time 🎉\n\n🎁 Prize -  {reward}\n\n🏆 Number of Winners - {num_winners}\n\n⏱ Ends in - {time_left_str}" , reply_markup=markup1)

def auto_message_update(message, chat_id, role_name, msg2):
    markup = telebot.types.ReplyKeyboardRemove()
    try:
        if message.text == "🚫Cancle":
            bot.delete_message(msg2.chat.id, msg2.id)
            bot.delete_message(message.chat.id, message.id)
            return

        count = int(message.text)

        roles.update_one(
            {'chat_id': chat_id, 'role_name': role_name},
            {'$set': {'message_count': count, 'is_auto_message': True}},
            upsert=True
        )

        bot.send_message(message.chat.id, "Auto Message has been updated.",reply_markup=markup)
        bot.delete_message(msg2.chat.id, msg2.id)
        bot.delete_message(message.chat.id, message.id)

    except Exception as e:
        print(f"Error updating auto_message for role: {e}")
        bot.send_message(message.chat.id, "An error occurred. Please try again later.", reply_markup=markup)

def auto_invite_update(message,chat_id,role_name,msg2):
    markup = telebot.types.ReplyKeyboardRemove()
    try:
        if message.text == "🚫Cancle":
            bot.delete_message(msg2.chat.id,msg2.id)
            bot.delete_message(message.chat.id,message.id)
            return
        count = int(message.text)

        roles.update_one(
            {'chat_id': chat_id, 'role_name': role_name},
            {'$set': {'invite_count': count , 'is_auto_invite':True }},
            upsert=True
        )
        data = invites.find({'chat_id':chat_id})
        if data:
            for da in data:
                user_id = da['user_id']
                regular_count = da['regular_count']
                if regular_count >= count :
                    roles.update_one({'chat_id': chat_id, 'user_id': user_id}, {'$addToSet': {'roles': role_name}}, upsert=True)
                    roles.update_one({'chat_id':chat_id,'role_name':role_name},
                             {'$inc':{'count':1}},upsert=True)
        bot.send_message(message.chat.id,"Auto Invite has been added",reply_markup=markup)
        bot.delete_message(msg2.chat.id,msg2.id)
        bot.delete_message(message.chat.id,message.id)
    except Exception as e:
        print(f"Error creating role: {e}")
        bot.send_message(message.chat.id, "An error occurred. Please try again later.", reply_markup=markup)

def create_role(message,chat_id,msg2):
    markup = telebot.types.ReplyKeyboardRemove()
    try:
        if message.text == "🚫Cancle":
            bot.delete_message(msg2.chat.id,msg2.id)
            bot.delete_message(message.chat.id,message.id)
            return
        role_name = message.text.split(' ')[0].lower()
        find = roles.find_one({'chat_id': chat_id, 'role_name': role_name})
        if find:
            bot.delete_message(msg2.chat.id,msg2.id)
            bot.delete_message(message.chat.id,message.id)
            bot.send_message(message.chat.id, f"The role '{role_name}' already exists.", reply_markup=markup)
            return
        role_id = str(uuid.uuid4())
        roles.update_one({'chat_id': chat_id,'role_id':role_id}, {'$set': {'role_name': role_name}, '$inc': {'count': 0}}, upsert=True)
        bot.send_message(message.chat.id, f"The role '{role_name}' has been successfully created.", reply_markup=markup)
        bot.delete_message(msg2.chat.id,msg2.id)
        bot.delete_message(message.chat.id,message.id)
    except Exception as e:
        print(f"Error creating role: {e}")
        bot.send_message(message.chat.id, "An error occurred. Please try again later.", reply_markup=markup)

def delete_role(message,chat_id, role_name,msg2):
    markup = telebot.types.ReplyKeyboardRemove()
    try:
        if message.text == "🚫Cancle":
            bot.delete_message(msg2.chat.id, msg2.id)
            bot.delete_message(message.chat.id, message.id)
            return
        elif message.text == "🗑Delete":
            role_deleted = False
            users_with_role = roles.find({'chat_id': chat_id, 'roles': role_name})

            for user in users_with_role:
                user_id = user['user_id']

                roles.update_one({'chat_id': chat_id, 'user_id': user_id}, {'$pull': {'roles': role_name}})
                role_deleted = True

            roles.delete_one({'chat_id':chat_id,'role_name':role_name})
            if role_deleted:
                bot.send_message(msg2.chat.id, f"The {role_name} role has been removed from all users.", reply_markup=markup)
                bot.delete_message(msg2.chat.id, msg2.id)
                bot.delete_message(message.chat.id, message.id)
            else:
                bot.send_message(msg2.chat.id, f"No users have the {role_name} role.", reply_markup=markup)
                bot.delete_message(msg2.chat.id, msg2.id)
                bot.delete_message(message.chat.id, message.id)
    except Exception as e:
        print(f"Error deleting role: {e}")
        bot.send_message(message.chat.id, "An error occurred. Please try again later.", reply_markup=markup)

def add_how_to_get(message,chat_id,role_name,msg2):
    markup = telebot.types.ReplyKeyboardRemove()
    try:
        if message.text == "🚫Cancle":
            bot.delete_message(msg2.chat.id,msg2.id)
            bot.delete_message(message.chat.id,message.id)
            return
        find = roles.find_one({'chat_id': chat_id, 'role_name': role_name})
        how_to_get = message.text
        if find:
            bot.delete_message(msg2.chat.id,msg2.id)
            bot.delete_message(message.chat.id,message.id)
            roles.update_one({'chat_id': chat_id, 'role_name': role_name},{'$set':{'how_to_get':how_to_get}},upsert=True)
            bot.send_message(message.chat.id, f" How to get is now set for {role_name} ", reply_markup=markup)
    except Exception as e:
        print(f"Error creating role: {e}")
        bot.send_message(message.chat.id, "Error in setting how to get ion role", reply_markup=markup)

def change_role_name(message,old_role_name, chat_id,msg2):
    markup = telebot.types.ReplyKeyboardRemove()
    try:
        if message.text == "🚫Cancle":
            bot.delete_message(msg2.chat.id,msg2.id)
            bot.delete_message(message.chat.id,message.id)
            return
        role = roles.find_one({'chat_id': chat_id, 'role_name': old_role_name})
        new_role_name = message.text.split(" ")[0]
        if not role:
            bot.delete_message(msg2.chat.id,msg2.id)
            bot.delete_message(message.chat.id,message.id)
            bot.send_message(message.chat.id, f"The role '{old_role_name}' does not exist.",reply_markup=markup)
            return

        existing_role = roles.find_one({'chat_id': chat_id, 'role_name': new_role_name})
        if existing_role:
            bot.send_message(message.chat.id, f"The role '{new_role_name}' already exists. Please choose another name.",reply_markup=markup)
            bot.delete_message(msg2.chat.id,msg2.id)
            bot.delete_message(message.chat.id,message.id)
            return
        data = roles.find({'chat_id':chat_id,'roles':old_role_name})
        if data:
            for da in data:
                roles.update_one({'chat_id': chat_id, 'roles': old_role_name}, {'$set': {'roles': new_role_name}})
        roles.update_one({'chat_id': chat_id, 'role_name': old_role_name}, {'$set': {'role_name': new_role_name}})
        bot.send_message(message.chat.id, f"The role '{old_role_name}' has been successfully renamed to '{new_role_name}'.",reply_markup=markup)
        bot.delete_message(msg2.chat.id,msg2.id)
        bot.delete_message(message.chat.id,message.id)
    except Exception as e:
        print(f"Error changing role name: {e}")
        bot.send_message(message.chat.id,"An error occurred. Please try again later.",reply_markup=markup)

def leaderboard_invite(chat_id,sec,from_user):
    seven_days_ago = datetime.now() - timedelta(seconds=sec)
    data = invites.find({'chat_id':chat_id,'timestamp': {'$gte': seven_days_ago}})
    bot.send_message(from_user,"This Process may takes few seconds in collecting data from database")
    users = {}
    i = 0
    for da in data:
        if 'users' in da:
            for (user_id,daa) in da['users'].items():
                user_timestamp = daa['timestamp']
                if user_timestamp and user_timestamp >= seven_days_ago:
                    i = i + 1
        if i == 0:
            continue
        first_name = da['first_name']
        user_id = da['user_id']
        username = da['username']
        users[user_id] = {'first_name':first_name,'invites':i,'username':username}
        i = 0
    sorted_participants = sorted(users.items(), key=lambda x: x[1]['invites'], reverse=True)
    msg_text = "Requested invite leaderboad --:\n\n"
    for (user_id,data) in sorted_participants:
        i = i + 1
        msg_text += f"{i}. @{data['username']} - {data['invites']} invites\n"
        if i >= 10:
            break
    bot.send_message(from_user ,msg_text , parse_mode='HTML')

def invite_time(message,chat_id):
    markup = types.ReplyKeyboardRemove()
    if message.text == "🚫Cancle":
        bot.send_message(message.chat.id,"Action Cancled 🚫",reply_markup=markup)
        return
    duration = message.text
    duration_units = {"d": 86400, "h": 3600, "m": 60, "s": 1}
    try:
        duration = int(duration[:-1]) * duration_units[duration[-1]]
    except Exception:
        bot.send_message(message.from_user.id,"Error occur when convering time\ntry again use format: 1d,1h,1m,1s")
        bot.register_next_step_handler(message,invite_time,chat_id)
        return
    leaderboard_invite(chat_id,duration,message.from_user.id)

def get_price(crypto_symbol):
    url = f'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol={crypto_symbol}&convert=USD'
    headers = {'X-CMC_PRO_API_KEY': API_KEY}
    response = requests.get(url, headers=headers)
    data = response.json()
    if 'status' in data and data['status']['error_code'] == 400:
        return None
    try:
        price = data['data'][crypto_symbol]['quote']['USD']['price']
        percent_change_24h = data['data'][crypto_symbol]['quote']['USD']['percent_change_24h']
        return price, percent_change_24h
    except KeyError:
        return None

def generate_image(text, font_path, font_size, text_color, border_color, border_size, padding=10):
    # Create a new image with a transparent background
    # Calculate the required image size based on the text dimensions and padding
    font = ImageFont.truetype(font_path, size=font_size)
    words = text.split()
    max_word_width = max(font.getsize(word)[0] for word in words)
    text_height = sum(font.getsize(word)[1] for word in words)
    size = (max_word_width + 2 * padding, text_height + (len(words) - 1) * padding)

    image = Image.new('RGBA', size, (0, 0, 0, 0))

    # Draw the text onto the image
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_path, size=font_size)

    # Split the text into words
    text = text.replace("kaddu", "luldeep")
    words = text.split()

    # Set the initial y-coordinate
    y = padding // 2

    # Draw each word
    for word in words:
        # Determine the font size for this word
        word_font_size = font_size
        if len(word) > 6:
            extra_letters = len(word) - 6
            font_decrease_percent = extra_letters * 10
            word_font_size -= int(font_size * font_decrease_percent / 100)

        # Set the font for this word
        word_font = ImageFont.truetype(font_path, size=word_font_size)

        # Draw the word onto the image
        text_width, text_height = draw.textsize(word, font=word_font)
        x = (size[0] - text_width) / 2
        draw.text((x, y), word, fill=text_color, font=word_font, stroke_width=border_size, stroke_fill=border_color)

        # Update the y-coordinate for the next word
        y += word_font_size
    
    
    return image

def generate_sticker(text, font_path, font_size=100, text_color=(255, 255, 255), border_color=(0, 0, 0), border_size=10):
    image = generate_image(text, font_path, font_size, text_color, border_color, border_size)
    sticker_file = BytesIO()
    image.save(sticker_file, format='PNG')
    sticker_file.seek(0)
    return sticker_file

@bot.message_handler(commands=['local'])
def local(message):
    markup = types.InlineKeyboardMarkup()

    markup.row(
    types.InlineKeyboardButton('中文 中国 Chinese 🇨🇳', url='https://t.me/binaryxOfficial'),
    types.InlineKeyboardButton('हिन्दी Hindi India 🇮🇳', url='https://t.me/BinaryX_Hindi')
)
    markup.row(
    types.InlineKeyboardButton('Brazil Português 🇧🇷', url='https://t.me/BinaryXChat'),
    types.InlineKeyboardButton('Bengali বাংলা 🇧🇩', url='https://t.me/BinaryX_Bengali')  
)
    markup.row(
    types.InlineKeyboardButton('Arabic عربى ', url='https://t.me/BinaryX_Arabic'),
    types.InlineKeyboardButton('Turkish Türkçe ', url='https://t.me/BinaryXTurkeyOfficial')
)
    markup.row(
    types.InlineKeyboardButton('Indonesia 🇮🇩', url='https://t.me/BinaryXIndonesia'),
    types.InlineKeyboardButton('Pakistan ', url='https://t.me/binaryxurdu')
)
    bot.send_message(
        chat_id=message.chat.id,
        text="Join BinaryX local group 🌍",
        reply_markup=markup
        )

def save_chart(coin):
    url = f'https://api.coingecko.com/api/v3/coins/{coin}/ohlc?vs_currency=usd&days=1'
    if coin == "binaryx-2":
        symbol = "BNX"
    elif coin == "cyberdragon-gold":
        symbol = "GOLD"
    
    data = requests.get(url).json()
    for da in data:
        dt_object = datetime.utcfromtimestamp(da[0] / 1000)
        da[0] = dt_object.strftime("%Y-%m-%d %H:%M:%S")

    df = pd.DataFrame(
        {
            'time': [i[0] for i in data],
            'open': [i[1] for i in data],
            'high': [i[2] for i in data],
            'low': [i[3] for i in data],
            'close': [i[4] for i in data],
        }
    )

    df['time'] = pd.to_datetime(df['time'])
    df.set_index('time', inplace=True)

    if not os.path.exists("img"):
        os.mkdir("img")

    with Image.open("chart_bg.png") as bg_image:
        fig, ax = plt.subplots(figsize=(12, 7))
        plt.subplots_adjust(right=0.9)
        fpath = Path(mpl.get_data_path(), "/home/runner/binaryx/AbradeBold.ttf")

        mpf.plot(df, type='candle', ax=ax, style='yahoo', datetime_format='%H:%M')
        
        ax.set_title(f'{symbol}/USD Price Chart (Past 24 Hours)', color='#f3f5f4', font=fpath, fontsize=20)
        ax.set_xlabel('Time', color='#f3f5f4', font=fpath, fontsize=15)
        ax.set_ylabel('Price (USD)', color='#f3f5f4', font=fpath, fontsize=15)
        
        ax.tick_params(axis='x', colors='#f3f5f4')
        ax.tick_params(axis='y', colors='#f3f5f4')
        ax.spines['left'].set_color('#727886')
        ax.spines['left'].set_linewidth(2)
        ax.spines['bottom'].set_color('#727886')
        ax.spines['bottom'].set_linewidth(2)
        ax.spines['right'].set_color('#727886')
        ax.spines['right'].set_linewidth(2)
        ax.spines['top'].set_color('#727886')
        ax.spines['top'].set_linewidth(2)
        
        current_price = df['close'].iloc[-1]
        ax.axhline(y=current_price, color='red', linestyle='--', label='Current Price')
        ax.set_yticks(ax.get_yticks().tolist() + [current_price])
        tick_labels = ax.get_yticklabels()
        tick_labels[-1].set_color('red')
        ax.set_yticklabels(tick_labels)
        
        ax.set_facecolor('#181d33')

        fig.patch.set_facecolor('#181d33')
        fig.figimage(bg_image, xo=0, yo=0, alpha=0.5)
        plt.legend()

        image_path = "img/chart.png"
        plt.savefig(image_path)
        
    return image_path
  
@bot.message_handler(['bnxhistory'])
def bnx_handler(message):
    bot.send_chat_action(message.chat.id,'upload_document')
    coin = "binaryx-2"
    image_path = save_chart(coin)
    crypto_symbol = 'BNX'
    url = f'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol={crypto_symbol}&convert=USD'
    headers = {'X-CMC_PRO_API_KEY': API_KEY}
    response = requests.get(url, headers=headers)
    data = response.json()
    short = data['data'][crypto_symbol]['quote']['USD']
    price = short['price']
    per24 = short['percent_change_24h']
    per1 = short['percent_change_1h']
    per7 = short['percent_change_7d']
    vol = short['volume_24h']
    marcap = short['market_cap']
    csupply = data['data'][crypto_symbol]['circulating_supply']
    tsupply = data['data'][crypto_symbol]['total_supply']

    caption = f"<b>📈 BinaryX (BNX) Chart 📉</b>\n\n"
    caption += f"💰 <b>Price</b>: ${price:.3f}\n"
    caption += f"⚡️ <b>1hr Change</b>:   {per1:.2f}%\n"
    caption += f"🌙 <b>24hr Change</b>: {per24:.2f}%\n"
    caption += f"📅 <b>7d Change</b>:    {per7:.2f}%\n"
    caption += f"💹 <b>Volume</b>: ${vol:.2f}\n"
    caption += f"🏦 <b>Market Cap</b>: ${marcap:.2f}\n"
    caption += f"💼 <b>Circulating Supply</b>: ${csupply:.2f}\n"
    caption += f"📊 <b>Total Supply</b>: ${tsupply:.2f}"

    markup = types.InlineKeyboardMarkup()
    markup.row(types.InlineKeyboardButton('💠 Buy BNX 💠', url='https://pancakeswap.finance/swap?outputCurrency=0x5b1f874d0b0C5ee17a495CbB70AB8bf64107A3BD'))
    with open(image_path, 'rb') as chart_image:
        bot.send_photo(message.chat.id,chart_image ,caption=caption,parse_mode='HTML',reply_markup=markup)


@bot.message_handler(['goldhistory'])
def bnx_handler(message):
    bot.send_chat_action(message.chat.id,'upload_document')
    coin = "cyberdragon-gold"
    image_path = save_chart(coin)
    coin_id = 12082
    url = f'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?id={coin_id}'
    headers = {'X-CMC_PRO_API_KEY': API_KEY}
    response = requests.get(url, headers=headers)
    data = response.json()
    short = data['data'][str(coin_id)]['quote']['USD']
    price = short['price']
    per24 = short['percent_change_24h']
    per1 = short['percent_change_1h']
    per7 = short['percent_change_7d']
    vol = short['volume_24h']
    marcap = short['market_cap']
    csupply = data['data'][str(coin_id)]['circulating_supply']
    tsupply = data['data'][str(coin_id)]['total_supply']

    text = "<b>Cyber Dragron Gold (GOLD)</b>"
    text += f"\n\n<b>Price</b>: ${price:.6f}"
    text += f"\n<b>1hr Change</b>:   {per1:.2f}%"
    text += f"\n<b>24hr Change</b>: {per24:.2f}%"
    text += f"\n<b>7d Change</b>:    {per7:.2f}%"
    text += f"\n<b>Volume</b>: ${vol:.2f}"
    text += f"\n<b>Total Supply</b>: ${tsupply}"
    markup = types.InlineKeyboardMarkup()
    markup.row(types.InlineKeyboardButton('💠 Buy GOLD 💠', url='https://pancakeswap.finance/swap?outputCurrency=0xb3a6381070b1a15169dea646166ec0699fdaea79'))
    with open(image_path, 'rb') as chart_image:
        bot.send_photo(message.chat.id,chart_image ,caption=text,parse_mode='HTML',reply_markup=markup)


@bot.message_handler(commands=['gold','GOLD'])
def gold(message):
        coin_id = 12082
        args = message.text.split()[1:]
        url = f'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?id={coin_id}'
        headers = {'X-CMC_PRO_API_KEY': API_KEY}
        response = requests.get(url, headers=headers)
        data = response.json()
        # Extract the price from the response
        price = data['data'][str(coin_id)]['quote']['USD']['price']
        percent_change_24h = data['data'][str(coin_id)]['quote']['USD']['percent_change_24h']
        response_text = f"💸 Current Price💲 \n\n💠<b>GOLD</b> :<code> ${price:,.5f}</code> "
        if percent_change_24h is not None:
            change_24h_text = f"{percent_change_24h:.2f}%"
            if percent_change_24h > 0:
                response_text += f" (🟢{change_24h_text})"
            elif percent_change_24h < 0:
                response_text += f" (🔴{change_24h_text})"
            else:
                response_text += f" ({change_24h_text})"
        if len(args) == 1:
            amount, = args
        if len(args) != 0:
            try:
                amount = int(amount)
            except ValueError:
                bot.reply_to(message, "You shoud correct amount \nexample : /gold 250")
                return
        if len(args) == 1:
            url = f'https://pro-api.coinmarketcap.com/v1/tools/price-conversion?amount={amount}&id=12082&convert=usd'
            headers = {'X-CMC_PRO_API_KEY': API_KEY}
            response = requests.get(url, headers=headers)
            data = response.json()
            cnv_amt = data['data']['quote']['USD']['price']
            response_text += f"\n----------------------------------\n💠{amount} <b>GOLD</b> = ${cnv_amt:,.2f}"
            bot.send_message(message.chat.id, response_text, parse_mode='HTML')
        else:
            
            bot.send_message(message.chat.id, response_text, parse_mode='HTML')

@bot.message_handler(commands=['social'])
def social(message):
    bot.send_message(
        chat_id=message.chat.id,
        text="👺 Twitter - https://twitter.com/binary_x \n\n👺 Discord - https://discord.gg/binaryx",
        disable_web_page_preview=True
        )

@bot.message_handler(commands=['website'])
def website(message):
    bot.send_message(
        chat_id=message.chat.id,
        text="website -- https://binaryx.pro"
        )

@bot.message_handler(commands=['BNX','bnx'])
def bnx(message):
        symbol = "BNX"
        args = message.text.split()[1:]
        result = get_price(symbol)
        price, percent_change_24h = result
        response_text = f"💸 Current Price💲 \n\n💠<b>{symbol}</b> :<code> ${price:,.2f}</code> "
        if percent_change_24h is not None:
            change_24h_text = f"{percent_change_24h:.2f}%"
            if percent_change_24h > 0:
                response_text += f" (🟢{change_24h_text})"
            elif percent_change_24h < 0:
                response_text += f" (🔴{change_24h_text})"
            else:
                response_text += f" ({change_24h_text})"
        if len(args) == 1:
            amount, = args
        if len(args) != 0:
            try:
                amount = int(amount)
            except ValueError:
                bot.reply_to(message, "You shoud correct amount \nexample : /bnx 25")
                return
        if len(args) == 1:
            url = f'https://pro-api.coinmarketcap.com/v1/tools/price-conversion?amount={amount}&symbol=BNX&convert=USD'
            headers = {'X-CMC_PRO_API_KEY': API_KEY}
            response = requests.get(url, headers=headers)
            data = response.json()
            if 'status' in data and data['status']['error_code'] == 400:
                return None
            converted_amount = data['data']['quote']['USD']['price']
            response_text += f"\n----------------------------------\n💠{amount} <b>BNX</b> = <code>${converted_amount:,.2f}</code>"
            bot.send_message(message.chat.id, response_text, parse_mode='HTML')
        else:
            bot.send_message(message.chat.id, response_text, parse_mode='HTML')

@bot.message_handler(commands=['giveaway'])
def giveaway_handler(message):
    chat_id = message.chat.id
    chat_members = bot.get_chat_administrators(chat_id)
    user_id = message.from_user.id
    is_admin = any(member.user.id == user_id and member.status in ['creator', 'administrator'] for member in chat_members)

    if not is_admin:
        bot.reply_to(message, "You must be an administrator to use this command.")
        return

    args = message.text.split()[1:]
    if args == []:
        bot.reply_to(message, "The command format is invalid.")
        return
    duration_units = {"d": 86400, "h": 3600, "m": 60, "s": 1}
    is_how_to = False
    if len(args) >= 3:
        try:
            amount, num_winners, duration = args[:3]
            role = None
            amount = amount.replace("_"," ")
            duration = int(duration[:-1]) * duration_units[duration[-1]]
        except (ValueError, KeyError, IndexError):
            bot.reply_to(message, "The command format is invalid. Usage: /giveaway <prize_amount> <currency> <number_of_winners> <duration> <*role> <*description>")
            return
    else:
        bot.reply_to(message, "The command format is invalid.")
        return

    if len(args) == 4:
        role = args[3]
        data = roles.find_one({'chat_id':message.chat.id,'role_name':role})
        if data:
            if 'how_to_get' in data:
                is_how_to = True
                button12 = InlineKeyboardButton(f"How to get {role}", callback_data=f"giveaway_how_to:{role}:{chat_id}")
        else:
            bot.reply_to(message,f"The {role} does not exist in this chat.")
            return
    # Generate a unique identifier for the giveaway
    giveaway_id = str(uuid.uuid4())

    # Store the giveaway data using the unique identifier
    document = {
        "giveaway_id": giveaway_id,
        "chat_id": chat_id,
        "amount": amount,
        "num_winners": num_winners,
        "duration": duration,
        "role": role,
        "participants": [],
        "last_refresh_time": time.time(),
        "winners":[],
        "message_id": message.message_id + 1,
        "is_edit":False
    }

    giveaways.insert_one(document)

    time_left = duration
    time_left_str = f"{time_left // 86400}d:{(time_left % 86400) // 3600}h:{(time_left % 3600) // 60}m:{time_left % 60}s"
    message_text = f"🎉 Lottery Time 🎉\n\n🎁 Prize -  {amount}\n\n🏆 Number of Winners - {num_winners}\n\n⏱ Ends in - {time_left_str}"

    if role :
        message_text += f"\n\nTo participate in this lottery, you need to have the {role} role."

    url = f"https://t.me/Binaryx_robot?start={giveaway_id}"
    
    text = f"Join"
    leave_call = f"leave_giveaway:{giveaway_id}"
    refresh_text = f"Refresh ({time_left_str})"
    refresh_call = f"Refresh:{giveaway_id}"
    reply_markup = telebot.types.InlineKeyboardMarkup()
    reply_markup.add(telebot.types.InlineKeyboardButton(text,url=url))
    reply_markup.add(telebot.types.InlineKeyboardButton("Leave", callback_data=leave_call))
    reply_markup.add(telebot.types.InlineKeyboardButton(refresh_text, callback_data=refresh_call))

    if is_how_to:
        reply_markup.add(button12)
    msg = bot.send_message(chat_id, message_text, reply_markup=reply_markup)
    # bot.delete_message(message.chat.id, message.id)
    giveaways.update_one({'giveaway_id': giveaway_id},{'$set':{'message_id':msg.id}},upsert=True)
    time_thread = threading.Thread(target=time_check)
    time_thread.start()

def end_giveaway(giveaway_id):
    giveaway = giveaways.find_one({"giveaway_id": giveaway_id})
    if giveaway:
        chat_id = giveaway["chat_id"]
        if len(giveaway["participants"]) < int(giveaway["num_winners"]):
            message_text = "There are not enough participants to select winners. The lottery event has been canceled."
            giveaway_id2 = str(uuid.uuid4())
            giveaways.update_one({'giveaway_id':giveaway_id},{'$set': {'giveaway_id': giveaway_id2 ,'is_done':True}},upsert=True)
            bot.send_message(chat_id, message_text)
            return
        winners = []
        for i in range(int(giveaway["num_winners"])):
            winner = random.choice(giveaway["participants"])
            winners.append(winner)
            giveaway["participants"].remove(winner)
        message_text = f"The lottery with a value of {giveaway['amount']} has ended. The list of winners is as follows:"
        giveaways.update_one({'giveaway_id':giveaway_id},{'$set': {'winners': winners }},upsert=True)
        for winner in winners:
            member = bot.get_chat_member(chat_id, winner)
            first_name = member.user.first_name
            message_text += f"\n🔹<a href='tg://user?id={member.user.id}'>{first_name}</a> - @{member.user.username}"
        bot.send_message(chat_id, message_text , parse_mode='HTML')

        giveaway_id2 = str(uuid.uuid4())
        giveaways.update_one({'giveaway_id':giveaway_id},{'$set': {'giveaway_id': giveaway_id2 ,'is_done':True}},upsert=True)

@bot.message_handler(['addtwi'])
def command_add(message):
    chat_id = message.chat.id
    if message.chat.id in persons['twitter']:
        bot.send_message(message.chat.id,"this group is already added for Tweets of Binary_x")
        return
    persons['twitter'].append(message.chat.id)
    with open(list_file, 'w') as f:
        json.dump(persons, f)
    bot.send_message(message.chat.id,f"Bot will send latest Tweets of Binary_x Here .")

@bot.message_handler(commands=['quiz'])
def quiz_handler(message):
    create_quiz(message,message.from_user.id)

@bot.message_handler(commands=['quies'])
def starts_handler(message):
    if message.text == "/quies":
        return
    id = message.text.split(" ")[1]
    start_quiz(id,message.chat.id,message.id)

@bot.message_handler(commands=['quiz_all','quizall'])
def edit_quiz(message):
    user_id = message.from_user.id
    data = quizs.find({'user_id':user_id})
    if data:
        msg_txt = "Your all quizs\n\n"
        i = 1
        markup = InlineKeyboardMarkup()
        for dat in data:
            quiz_id = dat['quiz_id']
            title = dat['title']
            time_left = dat.get('time_limit',"Not Set")
            questions = dat.get('questions',{})
            button = InlineKeyboardButton(title,callback_data=f"edit_quiz:{quiz_id}")
            markup.add(button)
            msg_txt += f"{i}. {title}\n❓{len(questions)} questions ▪️ ⏱ {time_left} sec\n\n"
            i = i + 1
    bot.send_message(message.chat.id,msg_txt,reply_markup=markup)

@bot.message_handler(commands=['stic'])
def handle_text_message(message):
    if len(message.text.split(' ')) > 1:
        text = message.text.split(' ', 1)[1]
    else:
        text = "Binaryx "

    font_path = os.path.join(os.getcwd(), "AbradeBold.ttf")

    sticker_file = generate_sticker(text, font_path)
    # Send the new sticker back to the user
    bot.send_sticker(message.chat.id, sticker_file)


@bot.message_handler(['stoptwi'])
def command_add(message):
    if message.chat.id not in persons['twitter']:
        bot.send_message(message.chat.id,"this group is not added for Tweets of Binary_x")
        return
    persons['twitter'].remove(message.chat.id)
    with open(list_file, 'w') as f:
        json.dump(persons, f)
    bot.send_message(message.chat.id,f"Bot will stop sending latest Tweets of Binary_x Here .")
        
def send_tweet_notifications(latest_tweet_id):
    while True:
        try:
            userr = snstwi.TwitterProfileScraper("binary_x")
            for i,tweet in enumerate(userr.get_items2()):
                if i>10:
                    break
                if tweet.id not in latest_tweet_id:
                    chat_ids = persons['twitter']
                    latest_tweet_id.append(tweet.id)
                    with open(tweet_file, 'w') as file:
                        json.dump(latest_tweet_id, file)
                    markup = types.InlineKeyboardMarkup()
                    markup.row(types.InlineKeyboardButton(f'{tweet.user.displayname} Tweet', url=f'{tweet.url}'))
                    # Check if the tweet is a reply
                    if tweet.inReplyToUser:
                        continue  # skip sending reply tweets
                    # Check if the tweet contains media
                    if tweet.media:
                        for media in tweet.media:
                            if isinstance(media, snstwi.Photo):
                                # Handle photo media
                                media_url = media.fullUrl
                                if "format=jpg" in media_url or "format=png" in media_url:
                                    # Download the photo
                                    response = requests.get(media_url)
                                    photo = response.content
                                    caption = f"<a href='{tweet.url}'>{tweet.user.displayname}</a>\n\n{tweet.rawContent[:-23]}"
                                    for chat_id in chat_ids:
                                        try:
                                            send_photo = bot.send_photo(chat_id, photo , caption=caption, parse_mode='HTML',reply_markup=markup)
                                            bot.pin_chat_message(send_photo.chat.id, send_photo.message_id,disable_notification=True)
                                            bot.delete_message(send_photo.chat.id,send_photo.message_id+1)
                                        except Exception as e:
                                            continue
                            elif isinstance(media, snstwi.Video):
                                # Handle video media
                                highest_bitrate = 0
                                highest_bitrate_variant = None
                                for variant in media.variants:
                                    if variant.contentType == 'video/mp4' and variant.bitrate and variant.bitrate > highest_bitrate:
                                        highest_bitrate = variant.bitrate
                                        highest_bitrate_variant = variant
                                if highest_bitrate_variant:
                                    video_url = highest_bitrate_variant.url
                                    # Send the video
                                    caption = f"<a href='{tweet.url}'>BinaryX</a>\n\n{tweet.rawContent[:-23]}"
                                    for chat_id in chat_ids:
                                        try:
                                            send_video = bot.send_video(chat_id, video=video_url, caption=caption, parse_mode='HTML',reply_markup=markup)
                                            bot.pin_chat_message(send_video.chat.id, send_video.message_id,disable_notification=True)
                                            bot.delete_message(send_video.chat.id,send_video.message_id+1)
                                        except Exception as e:
                                            continue
                    elif tweet.quotedTweet:
                        if tweet.quotedTweet.media:
                            for media in tweet.quotedTweet.media:
                                        if isinstance(media, snstwi.Photo):
                                            # Handle photo media
                                            media_url = media.fullUrl
                                            if "format=jpg" in media_url or "format=png" in media_url:
                                                # Download the photo
                                                response = requests.get(media_url)
                                                photo = response.content
                                                caption = f"<a href='{tweet.url}'>{tweet.user.displayname} [Quote Tweeted]</a>\n\n{tweet.rawContent}\n-------------\n{tweet.quotedTweet.rawContent[:-23]}"
                                                for chat_id in chat_ids:
                                                    try:
                                                        send_photo = bot.send_photo(chat_id, photo, caption=caption, parse_mode='HTML',reply_markup=markup)
                                                        bot.pin_chat_message(send_photo.chat.id, send_photo.message_id,True)
                                                        bot.delete_message(send_photo.chat.id,send_photo.message_id+1)
                                                    except Exception as e:
                                                        continue
                                        elif isinstance(media, snstwi.Video):
                                            # Handle video media
                                            highest_bitrate = 0
                                            highest_bitrate_variant = None
                                            for variant in media.variants:
                                                if variant.contentType == 'video/mp4' and variant.bitrate and variant.bitrate > highest_bitrate:
                                                    highest_bitrate = variant.bitrate
                                                    highest_bitrate_variant = variant
                                            if highest_bitrate_variant:
                                                video_url = highest_bitrate_variant.url
                                                # Send the video
                                                caption = f"<a href='{tweet.url}'>BinaryX</a>\n\n{tweet.rawContent}\n-------------\n{tweet.quotedTweet.rawContent[:-23]}"
                                                for chat_id in chat_ids:
                                                    try:
                                                        send_video = bot.send_video(chat_id, video=video_url, caption=caption, parse_mode='HTML',reply_markup=markup)
                                                        bot.pin_chat_message(send_video.chat.id, send_video.message_id,disable_notification=True)
                                                        bot.delete_message(send_video.chat.id,send_video.message_id+1)
                                                    except Exception as e:
                                                        continue
                        else:
                            if tweet.quotedTweet.rawContent:
                                # Send a notification with tweet details
                                        message1 = f"<a href='{tweet.url}'>{tweet.user.displayname} [Quote Tweeted]</a>\n\n{tweet.rawContent}\n-------------\n{tweet.quotedTweet.rawContent}"
                                        for chat_id in chat_ids:
                                            try:
                                                send_message = bot.send_message(chat_id, text=message1, parse_mode='HTML', disable_web_page_preview=True,reply_markup=markup)
                                                bot.pin_chat_message(send_message.chat.id, send_message.message_id)
                                                bot.delete_message(send_message.chat.id, send_message.id+1)
                                            except Exception as e:
                                                continue
                    else:
                        if tweet.rawContent:
                            # Send a notification with tweet details
                            message1 = f"<a href='{tweet.url}'>{tweet.user.displayname}</a>\n\n{tweet.rawContent}"
                            for chat_id in chat_ids:
                                try:
                                    send_message = bot.send_message(chat_id, text=message1, parse_mode='HTML', disable_web_page_preview=True,reply_markup=markup)
                                    bot.pin_chat_message(send_message.chat.id, send_message.message_id,disable_notification=True)
                                    bot.delete_message(send_message.chat.id,send_message.message_id+1)
                                except Exception as e:
                                    continue
        except Exception as e:
            print(f"An error occurred: {e}")
            bot.send_message(1443989714,f"{e} \n\n\n\n\n {latest_tweet_id}")
            time_thread = threading.Thread(target=send_tweet_notifications, args=(latest_tweet_id,))
            time_thread.start()
        time.sleep(600)

@bot.inline_handler(lambda query: True)
def handle_inline_query(query):
    try:
        results = []
        user_id = query.from_user.id
        data = queries.find_one({'user_id': user_id})
        count = 0
        if query.query and data and 'results' in data:
            for result in data['results']:
                if query.query in result['title']:
                    count += 1
                    results.append(
                        types.InlineQueryResultArticle(
                            id=result['id'],
                            title=result['title'],
                            input_message_content=types.InputTextMessageContent(
                                message_text=result['input_message_content']['message_text']
                            )
                        )
                    )
        results.append(types.InlineQueryResultArticle(id=112233,title=f"Total Giveaways Found = [{count}]",input_message_content=types.InputTextMessageContent("hello")))
        bot.answer_inline_query(query.id, results)

    except Exception as e:
        # Log the error for debugging purposes (you can use your preferred logging mechanism)
        print(f"Error processing inline query: {e}")
        pass

def project_matthew(message , call):

    text = "<b>Project Matthew: To the Moon and Beyond</b> <a href='https://lightning-mole-a4a.notion.site/image/https%3A%2F%2Fs3-us-west-2.amazonaws.com%2Fsecure.notion-static.com%2F393ecc80-9898-4004-b0a7-93f914cfebe6%2F2_(8).jpg?id=4000b3ea-dacd-46d3-be99-c568a55c3eee&table=block&spaceId=64eb586d-36fe-4a9b-9d84-2bc0caf4d030&width=2000&userId=&cache=v2'>🚀</a>🌗"
    text +="\n\n🔘 <b>Trailer video </b>:"
    text +="\nhttps://youtu.be/bFdHYvQ-2mM"
    text +="\n\n🔘 <b>Beginners Guide: </b>"
    text += "\nhttps://lightning-mole-a4a.notion.site/Project-Matthew-Wiki-12d34bc749c2425f9143d263c63461c6"
    text += "\n\n🔘 <b>Website :</b>"
    text += "\nhttps://www.projectmatthew.io"
    markup = types.InlineKeyboardMarkup()
    markup.row(types.InlineKeyboardButton('🔹 Account Registration', url='https://lightning-mole-a4a.notion.site/Account-Registration-f075f7b02f844f989a7f83b7697d6acb'))
    markup.row(types.InlineKeyboardButton('🔹 How to get Matthew Land (NFT)?', url='https://lightning-mole-a4a.notion.site/How-to-get-Matthew-Land-NFT-7e195dfccbde4b9ba0d7199df7bed4c4'))
    markup.row(types.InlineKeyboardButton('🗒 Whitepaper',url='https://lightning-mole-a4a.notion.site/Project-Matthew-Whitepaper-1-0-82d069497ecb46bd962647630b1f697d'))
    if call:
        markup.row(types.InlineKeyboardButton('Return', callback_data='Games'))
        bot.edit_message_text(text,call.message.chat.id,call.message.message_id,reply_markup=markup,parse_mode='HTML')
    elif message:
        bot.send_message(message.chat.id,text,parse_mode='HTML',reply_markup=markup)


def ai_hero(message , call):

    text = "<b>AI HERO : A multiplayer battle royale text adventure game.</b> <a href='https://binaryx.pro/game/detail/5/_next/image?url=https%3A%2F%2Fs3.ap-northeast-1.amazonaws.com%2Fbinaryx-game%2Fbinaryx-web-dev%2F13c50a9c-df1a-4deb-9805-a675986c56114855888062745215632.jpg&w=3840&q=75'>🚀</a>🌗"
    text +="\n\n🔘 <b>Beginners Guide: </b>"
    text += "\nhttps://lightning-mole-a4a.notion.site/Ai-Hero-Wiki-89677111a6f948e886f2749f17c24cb2"
    text += "\n\n🔘 <b>Website :</b>"
    text += "\nhttps://aihero.binaryx.pro/"
    markup = types.InlineKeyboardMarkup()
    markup.row(types.InlineKeyboardButton('🗒 Wiki',url='https://lightning-mole-a4a.notion.site/Ai-Hero-Wiki-89677111a6f948e886f2749f17c24cb2'))
    if call:
        markup.row(types.InlineKeyboardButton('Return', callback_data='Games'))
        bot.edit_message_text(text,call.message.chat.id,call.message.message_id,reply_markup=markup,parse_mode='HTML')
    elif message:
        bot.send_message(message.chat.id,text,parse_mode='HTML',reply_markup=markup)


def pancake_swap_game(message , call):
    
    text = "<b>PANCAKE SWAP : Step into world of hyper-casual gaming fun! </b> <a href='https://pbs.twimg.com/media/GAp8SFTbAAAEAWR?format=jpg&name=900x900'>🎢</a>🌗"
    text +="\n\n🔘 <b>Beginners Guide: </b>"
    text += "\nhttps://binary-x.medium.com/pancakemayor-is-live-how-to-win-your-share-of-7000-cake-and-more-e45619ce5662"
    text += "\n\n🔘 <b>Play Now :</b>"
    text += "\nhttps://pancakeswap.games/project/binary-x"
    markup = types.InlineKeyboardMarkup()
    markup.row(types.InlineKeyboardButton('🗒 Wiki',url='https://binary-x.medium.com/pancakemayor-is-live-how-to-win-your-share-of-7000-cake-and-more-e45619ce5662'))
    if call:
        markup.row(types.InlineKeyboardButton('Return', callback_data='Games'))
        bot.edit_message_text(text,call.message.chat.id,call.message.message_id,reply_markup=markup,parse_mode='HTML')
    elif message:
        bot.send_message(message.chat.id,text,parse_mode='HTML',reply_markup=markup)




def time_check():
    with lock:
        time.sleep(10)
        while True:
            i = 1
            giveawayes = giveaways.find()
            for giveaway in giveawayes:
                if 'is_done' in giveaway:
                    continue
               
                y = int(giveaway["duration"])
                y -= 10
                i += 1
                time_left = y
                giveaway_id = giveaway['giveaway_id']
                giveaways.update_one({'giveaway_id': giveaway_id}, {'$set': {'duration': y}}) 
                if time_left <= 0:
                    end_giveaway(giveaway_id)
                if 'is_edit' in giveaway and giveaway['is_edit'] is True:
                    chat_id = giveaway['chat_id']
                    msg_id = giveaway['message_id']
                    num_win = len(giveaway['participants'])
                    message_text = f"Number of users join - {num_win} "
                    if 'del_id' in giveaway:
                        bot.delete_message(chat_id,giveaway['del_id'])
                    msg = bot.send_message(chat_id,message_text,reply_to_message_id=msg_id)
                    giveaways.update_one({'giveaway_id':giveaway_id},{'$set':{'is_edit':False,'del_id':msg.id}},upsert=True)
            if i == 1:
                return False
            time.sleep(10)

time_thread = threading.Thread(target=time_check)
time_thread.start()

with open(tweet_file, 'r') as file:
    latest_tweet_id = json.load(file)

# time_thread = threading.Thread(target=send_tweet_notifications,args=(latest_tweet_id,))
# time_thread.start()

print("ok i am working")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # Handle button clicks
    if message.text == 'CNFT 💠' or message.text == '/cnft':
        text = "<b>What's the CNFT?</b>\n\n- BinaryX Commemorative NFT (CNFT in short)  will be used as credentials to users’ participation in community building. It’s untransferable. It’s a kind of soul-bound token and like POAP to some extent.\n\n"
        text += "<b>What can the CNFTs be used for ?</b>\n\n- Users will be airdropped tokens depending on the CNFT they got for a new period."
        text += "\nTo check the latest exchange ratio:  <a href='https://lightning-mole-a4a.notion.site/ce066fa58bd84be8b9df326ca86572db?v=b3f54e1c419e43f1868426109c6108c6'>CNFT / BNX & BNXCExchange Rate Table</a>"
        text += "\n\n- We'll also value the opinions of our community contributors with the CNFT holders. More CNFTs, more voting power in the off-chain or off-website DAO proposal voting.\n<a href='https://bit.ly/3eaft0p'>CNFT voting</a>"
        text += "\n<a href='https://lightning-mole-a4a.notion.site/DAO-2-0-entry-Incentives-1db6b804f64c43228c6a66370f92df9b'>For latest CNFT info</a>"
        text += "\n<a href='https://galxe.com/BinaryX/campaign/GCVQnUt8Fb'>Claim link</a>"
        bot.send_message(message.chat.id,text,parse_mode='HTML',disable_web_page_preview=True)
    elif message.text == 'Match Mode 💠':
        text = "<b>⚔️Are you a fan of CyberChess Match Mode? Are you struggling to find an opponent?</b> \n\nWe have created a club, join now, find your opponent and fight together.\nThe club sends out a large amount of CNFT in different ways every week.\n\n"
        text += "🔗 https://t.me/MatchMode\n\n"
        text += "Here are some commands which will help you in event. \n👉<code>/won</code> - \n1️⃣ choose your rank .\n2️⃣ submit screenshot as proof . Points will add auto \n👉<code>/leaderboard</code> - this will show current leaderboard "
        bot.reply_to(message, text,parse_mode = 'HTML',disable_web_page_preview = True)
    elif message.text == 'Wiki 📖':
        text = "<b>CyberDragon Wiki</b>\n\nhttps://lightning-mole-a4a.notion.site/a9bdc9292c154131bac5af9e61fd66b1?v=2df2b1029eab436cb59f7ac8bf027838\n\n"
        text+= "<b>CyberChess Wiki</b>\n\nhttps://lightning-mole-a4a.notion.site/CyberChess-Wiki-8713d32de742480dae9b3432712dbfe3\n\n"
        text+= "<b>Project Matthew Wiki </b>\n\nhttps://lightning-mole-a4a.notion.site/Project-Matthew-Wiki-12d34bc749c2425f9143d263c63461c6"
        bot.send_message(message.chat.id,text,parse_mode='HTML')
    elif message.text == 'Notification Setting 🔔':
        text = 'iuhveaigbavjnv'
        markup = types.InlineKeyboardMarkup()
        twinoti = "Twitter Notification"
        events = "Community Event"
        person = persons['twitter']
        person2 = persons['cnft']
        if message.from_user.id in person:
            twinoti+= "🔔"
        else:
            twinoti += "🔕"
        if message.from_user.id in person2:
            events+= "🔔"
        else:
            events += "🔕"
        markup.row(
            types.InlineKeyboardButton(f'{twinoti}',callback_data='twinoti')
        )
        markup.row(
            types.InlineKeyboardButton(f'{events}',callback_data='cnoti')
        )
        bot.send_message(message.chat.id,  "Notification Setting 🔔 \n\nif you want to get twitter notification in your group\n1️⃣ Add this bot in your group as admin\n2️⃣ send /addtwi cmd in your group \nbot will start sending notification to your group\nif you want to stop just send /stoptwi " , reply_markup=markup)
    elif message.text == 'Roadmap 🛤' or 'roadmap' in message.text.lower() :
        file_id = 'BAACAgUAAxkBAAIHJmSIlAbusTFG2fG88Cuo4zQjKoOcAAKhCwACnx9JVDu_0CHafchiLwQ'
        bot.send_video(message.chat.id,file_id,caption="<b>BinaryX 2023 RoadMap - Level Up Your Game</b>",parse_mode='HTML')
    elif message.text == "Project Matthew 🚀" or "project matthew" in message.text.lower():
        project_matthew(message,None)
    elif message.text == "AI HERO 🏆" or "ai hero" in message.text.lower():
        ai_hero(message,None)
    elif message.text == "Pancakeswap Mayor 🥞🌟" or "pancakeswap" in message.text.lower():
        pancake_swap_game(message,None)

# keep_alive()
bot.polling(non_stop=True, interval=0) 