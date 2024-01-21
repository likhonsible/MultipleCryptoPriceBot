import os
import json
from pymongo import MongoClient
import time
import threading
import csv
import concurrent.futures
import uuid
import threading
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

ext ="hey"

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]


credentials = ServiceAccountCredentials.from_json_keyfile_name("clientgsheet.json", scope)

client2 = gspread.authorize(credentials)

spreadsheet_id = "1kVIKphMbFy3iZLi71jlOtLmQB7J6ijis8G97xNIrSmQ"
spreadsheet = client2.open_by_key(spreadsheet_id)

worksheet0 = spreadsheet.get_worksheet(0)
worksheet1 = spreadsheet.get_worksheet(1)

password = '1Gwhiuum22x0hmqf'
cluster_url = 'mongodb+srv://adibnslboy:' + password + '@bnslboy.02zrow4.mongodb.net/'


client = MongoClient(cluster_url)


db = client['main2']

list_file = os.path.join(os.getcwd(), 'lists.json')

giveaways = db['giveaways']

collection = db['invites']

roles = db['roles']

owners = db['admins']

dices = db['dices']

kidz = db['users']

try:
    with open(list_file, 'r') as f:
        persons = json.load(f)
except FileNotFoundError:
    pass
    
from pyrogram import Client , filters ,types , enums 

API_ID = '1149607'
API_HASH = 'd11f615e85605ecc85329c94cf2403b5'

bot = Client("my_test", api_id=API_ID, api_hash=API_HASH, bot_token="6133256899:AAFdu-7c_Sd8vZ886rW3p_GAgaXgQZKF7rk")


@bot.on_message(filters.command(['start']) & filters.group)
def start_for_group(client , message):
    try:
        admins = bot.get_chat_members(message.chat.id,filter=enums.ChatMembersFilter.ADMINISTRATORS)
        for admin in admins:
            user_id = admin.user.id
            list = owners.find_one({'chat_id': message.chat.id})
            if list:
                adminlist = list['admins']
                if user_id not in adminlist:
                    owners.update_one(
                        {'chat_id': message.chat.id},
                        {'$addToSet':{'admins': user_id},'$set':{'chat_title': message.chat.title}},upsert=True
                    )
            else:
                owners.update_one(
                        {'chat_id': message.chat.id},
                        {'$addToSet':{'admins': user_id}},upsert=True
                    )
    except Exception:
        pass

@bot.on_message(filters.command(['start']) & filters.private)
def start_for_private(client, message):
    if message.text == "/start":
        return
    else:
        giveaway_id = message.text.split(" ")[1]
        print(giveaway_id)
        giveaway = giveaways.find_one({'giveaway_id':giveaway_id})
        if giveaway is None:
            bot.send_message(message.from_user.id, "Sorry, this giveaway is no longer active.")
            return
        if giveaway:
            user_id = message.from_user.id
            giveaway = giveaways.find_one({'giveaway_id':giveaway_id})
            chat_id = giveaway['chat_id']
            role = giveaway["role"]
            if role == None:
                pass
            else:
                role_user = roles.find_one({'chat_id':chat_id,'user_id':user_id,'roles':role})
                if role_user is None:
                    bot.send_message(user_id, f"To participate in this draw, you must have the {role} role.")
                    return
            if user_id in giveaway["participants"]:
                bot.send_message(user_id, "You have already participated in this giveaway.")
                return
            giveaway["participants"].append(user_id)
            giveaways.update_one({"giveaway_id": giveaway_id}, {"$set": {"participants": giveaway["participants"],'is_edit':True}})
            bot.send_message(user_id, "You have successfully participated in the giveaway.")

@bot.on_message(filters.command(['settings']) & filters.private)
def create_role(client,message):
    is_markup = False
    list = owners.find({'admins':message.from_user.id})
    #Select a Chat in which you want to create a role --
    msg_txt = """👉🏻 Select the group whose invitation data you want to get.

If your group as an administrator does not appear here:
 • Send /reload in the group and try again
 • The bot is not an administrator in this group"""
    markup = types.InlineKeyboardMarkup(inline_keyboard=[])
    i = 1
    if list:
        for list2 in list:
            chat = list2['chat_id']
            if 'chat_title' in list2:
                title = list2['chat_title']
            else:
                try:
                    details = bot.get_chat(chat)
                    title = details.title
                except Exception:
                    continue
            markup.inline_keyboard.append([types.InlineKeyboardButton(f"{title}",callback_data=f"chat_group:{chat}")])
            
            is_markup = True
            if i == 7:
                markup.inline_keyboard.append([types.InlineKeyboardButton(f"Next Page ->",callback_data=f"nxtPage:{i}")])
                break
            i += 1
    if is_markup:
        bot.send_message(message.chat.id,msg_txt,reply_markup=markup)
    else:
        bot.send_message(message.chat.id,msg_txt)

@bot.on_message(filters.command(['reload']) & filters.group)
def start_for_group(client , message):
    try:
        admins = bot.get_chat_members(message.chat.id,filter=enums.ChatMembersFilter.ADMINISTRATORS)
        for admin in admins:
            user_id = admin.user.id
            list = owners.find_one({'chat_id': message.chat.id})
            if list:
                adminlist = list['admins']
                if user_id not in adminlist:
                    owners.update_one(
                        {'chat_id': message.chat.id},
                        {'$addToSet':{'admins': user_id},'$set':{'chat_title': message.chat.title}},upsert=True
                    )
            else:
                owners.update_one(
                        {'chat_id': message.chat.id},
                        {'$addToSet':{'admins': user_id}},upsert=True
                    )
    except Exception:
        pass
    msg_text = '✅ Bot updated\n✅ The list of administrators has been updated'
    bot.send_message(message.chat.id,msg_text)

@bot.on_message(filters.left_chat_member)
def left_member(client, message):
    chat_id = message.chat.id
    left_member_id = message.left_chat_member.id
    inviter = collection.find_one(
        {'chat_id': chat_id, 'users': left_member_id}
    )
    if inviter:
        inviter_id = inviter['user_id']
        collection.update_one(
            {'chat_id': chat_id, 'user_id': inviter_id},
            {'$inc': {'regular_count': -1, 'left_count': 1}},
        )

def role_giver(chat_id , user_id):
    data = roles.find({"chat_id":chat_id})
    is_give_role = False
    for da in data:
        if 'role_name' in da:
            role_name = da['role_name']
            if 'is_auto_invite' in da and da['is_auto_invite'] == True:
                
                count = da['invite_count']
                da2 = collection.find_one({'chat_id':chat_id,'user_id':user_id})
                if da2:
                    invite_count = da2['regular_count']
                    if invite_count >= count :
                        is_give_role = True
                    else:
                        is_give_role = False
                else:
                    is_give_role = False
            # if 'is_auto_message' in da and da['is_auto_message'] == True:
            #     count = da['message_count']
            #     da2 = messages.find_one({'chat_id':chat_id,'user_id':user_id})
            #     if da2:
            #         messages_count = da2['msg_count']
            #         if messages_count >= count:
            #             is_give_role = True
            #         else:
            #             is_give_role = False
            #     else:
            #         is_give_role = False
            if is_give_role == True:
                data = roles.find_one({'chat_id': chat_id, 'user_id': user_id,'roles': role_name})
                if data:
                    return
                usser = bot.get_users(user_id)
                usser_name = usser.username
                roles.update_one({'chat_id': chat_id, 'user_id': user_id}, {'$addToSet': {'roles': role_name},'$set': {'first_name': usser_name}}, upsert=True)
                roles.update_one({'chat_id':chat_id,'role_name':role_name},
                             {'$inc':{'count':1}},upsert=True)
                is_give_role = False
              
@bot.on_chat_member_updated()
def members(client, message):
    chat_id = message.chat.id
    if message.invite_link:
        
        abc = owners.find_one({'chat_id':chat_id})
        if abc:
            if 'link_msg' in abc and abc['link_msg'] is True:
                if 'cnft_msg' in abc and abc['cnft_msg'] is True:
                    kid = kidz.find_one({'user_id':message.from_user.id})
                    if kid:
                        cnft_bal = kid['cnft_bal']
                        if cnft_bal >= 1:
                            check = "done"
                            pass
                        else:
                            check = "pending"
                            bot.send_message(message.chat.id,f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a> You need to have more than 1 cnft your wallet . ")
                    else:
                        check = "pending"
                        bot.send_message(message.chat.id,f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a> You need to add your wallet address and you need to have more than 1 cnft in that wallet .")
                else:
                    check = "done"
            else:
                return
        else:
            return
        invite_link = message.invite_link.invite_link
        data = collection.find_one({'chat_id': chat_id, 'invite_link': invite_link})
        if data:
            user_id = data['user_id']
            username2 = data['username']
            first_name2 = data['first_name']
            rows = []
            username = message.from_user.username
            if username is None:
                username = message.from_user.first_name
            if username2 is None:
                username = first_name2
            pydate = datetime.now().strftime('%Y-%m-%d')
            rows.append([username, invite_link,username2, message.chat.title,pydate])   
            existing_row_count = len(worksheet1.get_all_values())
            worksheet1.insert_rows(rows, existing_row_count + 1)
            update_invites(chat_id, user_id, message.new_chat_member.user, "invite",check)

@bot.on_message(filters.new_chat_members)
def chatmember(client, message):
    chat_id = message.chat.id
    abc = owners.find_one({'chat_id':chat_id})
    if abc:
        if 'add_msg' in abc and abc['add_msg'] is True:
            pass
        else:
            return
    else:
        return
    user_id = message.from_user.id
    new_members = message.new_chat_members

    for new_member in new_members:
        if user_id != new_member.id:
            update_invites(chat_id, user_id, new_member, "add","done")

def update_invites(chat_id, user_id, new_member, point,check):
    current_time = datetime.now()
    da = collection.find_one({'chat_id': chat_id, 'user_id': user_id})
    if da is None:
        da = {}
    users = da.get('users', {})
    try:
        us = bot.get_users(user_id)
        username = us.username
        first_name = us.first_name
    except Exception:
        pass
    
    users[str(new_member.id)] = {
        'username': new_member.username,
        'first_name': new_member.first_name,
        'timestamp': current_time,
        'status': check
    }
    
    status = str(new_member.status)

    common_update_data = {
        '$set': {'users': users,'timestamp':current_time}
    }
    if first_name is not None:
        common_update_data['$set']['username'] = username
        common_update_data['$set']['first_name'] = first_name
    if status in ["UserStatus.LAST_WEEK", "UserStatus.ONLINE", "UserStatus.OFFLINE", "UserStatus.RECENTLY"]:
        specific_update_data = {
            '$inc': {'total_count': 1, 'left_count': 0, 'fake_count': 0, 'g_count': 1},
            '$set': {'users': users}
        }
        
        if check == "done":
            specific_update_data['$inc']['regular_count'] = 1
        elif check == "pending":
            specific_update_data['$inc']['pending_count'] = 1
        if point == "invite":
            daa = owners.find_one({'chat_id':chat_id})
            if daa and 'send_msg' in daa and daa['send_msg'] is True:
                bot.send_message(chat_id,f"<a href='tg://user?id={user_id}'>{first_name}</a> invites <a href='tg://user?id={new_member.id}'>{new_member.first_name}</a>")
            specific_update_data['$inc']['invi_count'] = 1

        update_data = {**specific_update_data, **common_update_data}
        role_giver(chat_id, user_id)
    else:
        update_data = {
            '$inc': {'total_count': 1, 'fake_count': 1, 'regular_count': 0, 'left_count': 0, 'g_count': 0},
            '$set': {'users': users}
        }

    collection.update_one(
        {'chat_id': chat_id, 'user_id': user_id},
        update_data,
        upsert=True
    )
    if point == "add" or point == "invite":
        owners.update_one({'chat_id': chat_id}, {'$inc': {'user_count': 1, f'{point}_count': 1}})


@bot.on_message(filters.command(['invites']))
def invites_finder(client, message):
    chat_id = message.chat.id
    if message.text == '/invites' or '/invites@Binaryx_robot':
        user_id = message.from_user.id
        first_name = message.from_user.first_name
        inviter = collection.find_one(
            {'chat_id': chat_id, 'user_id': user_id})
        if inviter:
            invi_count = inviter.get('pending_count',0)
            t_count = inviter.get('total_count',0)
            r_count = inviter.get('regular_count',0)
            f_count = inviter.get('fake_count',0)
            l_count = inviter.get('left_count',0)

            text = f"User <a href='tg://user?id={user_id}'>{first_name}</a> currently have \n<b>{r_count}</b> invites. (<b>{t_count}</b> Regular,<b> {l_count}</b> left,<b> {f_count}</b> fake,{invi_count} pending)"
        else:
            text = f"No data found for user <a href='tg://user?id={user_id}'>{first_name}</a>"
        bot.send_message(chat_id, text)
    else:
        args = message.text.split(" ")[1:]
        text = "Here the requested Data\n\n"
        for user in args:
            try:
                member = bot.get_chat(user)
            except Exception:
                continue
            user_id = member.id
            first_name = member.first_name
            inviter = collection.find_one(
                {'chat_id': chat_id, 'user_id': user_id})
            if inviter:
                invi_count = inviter.get('pending_count',0)
                t_count = inviter.get('total_count',0)
                r_count = inviter.get('regular_count',0)
                f_count = inviter.get('fake_count',0)
                l_count = inviter.get('left_count',0)
                text += f"User <a href='tg://user?id={user_id}'>{first_name}</a> currently have \n<b>{r_count}</b> invites. (<b>{t_count}</b> Regular,<b> {l_count}</b> left,<b> {f_count}</b> fake,{invi_count} pending)\n\n"
            else:
                text += f"No data found for user <a href='tg://user?id={user_id}'>{first_name}</a>\n\n"
        bot.send_message(chat_id, text)

@bot.on_message(filters.command(['topinvites']))
def top_invites(client, message):
    chat_id = message.chat.id
    top_invites = collection.find(
        {"chat_id": chat_id}
    ).sort("regular_count", -1).limit(10)
    response = "Top 10 Invites:\n\n"
    for index, invite in enumerate(top_invites):
        user_id = invite["user_id"]
        invi_count = invite.get('pending_count',0)
        t_count = invite.get('total_count',0)
        r_count = invite.get('regular_count',0)
        if r_count == 0:
            continue
        f_count = invite.get('fake_count',0)
        l_count = invite.get('left_count',0)
        
        first_name = invite['first_name']
        response += f"{index + 1}. {first_name} , <b>{r_count}</b> Invites. ({invi_count} pending)\n"
    if response == "Top 10 Invites:\n\n":
        response = "No Data Found"

    bot.send_message(chat_id, response)

@bot.on_message(filters.command(['link']) & filters.group)
def create_invite_link(client, message):
    chat_id = message.chat.id
    abc = owners.find_one({'chat_id':chat_id})
    if abc:
        if 'link_msg' in abc and abc['link_msg'] is True:
            if 'cnft_msg' in abc and abc['cnft_msg'] is True:
                    kid = kidz.find_one({'user_id':message.from_user.id})
                    if kid:
                        cnft_bal = kid['cnft_bal']
                        if cnft_bal >= 1:
                            pass
                        else:
                            bot.send_message(message.chat.id,f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a> You need to have more than 1 cnft your wallet . ")
                            return
                    else:
                        bot.send_message(message.chat.id,f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a> You need to add your wallet address and you need to have more than 1 cnft in that wallet .")
                        return
        else:
            bot.send_message(chat_id,"Hey there! It looks like the admin hasn't set up the invite link for this group just yet. That means we can't invite new members using a link for now.")
            return
    else:
        bot.send_message(chat_id,"Hey there! It looks like the admin hasn't set up the invite link for this group just yet. That means we can't invite new members using a link for now.")
        return
    bot_member = bot.get_chat_member(chat_id, 6133256899)
    if bot_member.privileges.can_invite_users is False:
        bot.send_message(chat_id,"❌ Insufficient permissions for the robot, please grant at least the following admin permissions:\n- Invite members via link")
        return
    
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    data = collection.find_one({'chat_id': chat_id, 'user_id': user_id,'invite_link': {'$exists': True}})

    if data:
            link = data['invite_link']
            invite_count = data['invi_count']
            
            message_text = f"""🔗 <a href='tg://user?id={user_id}'>{first_name}</a> Your exclusive link:
<code>{link}</code> (Click to copy)

👉 Current Total Invitations {invite_count} Person ."""
            bot.send_message(chat_id, message_text)
    else:
            link = bot.create_chat_invite_link(
                chat_id, f"{first_name} by @Binaryx_Robot")
            invite_link = link.invite_link
            message_text = f"""🔗 <a href='tg://user?id={user_id}'>{first_name}</a> Your exclusive link:
<code>{invite_link}</code> (Click to copy)

👉 Current Total Invitations 0 Person ."""
            bot.send_message(chat_id, message_text)
            collection.update_one(
                {'chat_id': chat_id, 'user_id': user_id},
                {'$set': {'invite_link': invite_link,'invi_count':0,'username':message.from_user.username,'first_name':message.from_user.first_name}},
                upsert=True
            )
            owners.update_one({'chat_id':chat_id},{'$inc':{'link_count':1}},upsert=True)
            rows = []
            username = message.from_user.username
            if username is None:
                username = message.from_user.first_name
            pydate = datetime.now().strftime('%Y-%m-%d')
            rows.append([username, invite_link, message.chat.title,pydate])   
            existing_row_count = len(worksheet0.get_all_values())
            worksheet0.insert_rows(rows, existing_row_count + 1)

def delete_tracker():
    while True:
        data = collection.find()
        chats = []
        for dat in data:
            if 'chat_id' in dat:
                chat_id = dat['chat_id']
                if chat_id not in chats:
                    chats.append(chat_id)
        for chat_id in chats:
            try:
                members = bot.get_chat_members(chat_id)
                for member in members:
                    if member.user.is_deleted:
                        left_member_id = member.user.id
                        inviter = collection.find_one(
                            {'chat_id': chat_id, 'new_members_ids': left_member_id}
                        )
                        inviter2 = collection.find_one(
                            {'chat_id': chat_id, 'fake_members_ids': left_member_id}
                        )
                        if inviter:
                            inviter_id = inviter['user_id']

                            # Decrement the invite count for the inviter
                            collection.update_one(
                                {'chat_id': chat_id, 'user_id': inviter_id},
                                {'$inc': {'regular_count': -1, 'left_count': 1}},
                                {'$pull': {'new_members_ids': left_member_id}}
                            )
                        elif inviter2:
                            inviter_id = inviter['user_id']
                            collection.update_one(
                                {'chat_id': chat_id, 'user_id': inviter_id},
                                {'$inc': {'regular_count': 0, 'left_count': 1}},
                                {'$pull': {'fake_members_ids': left_member_id}}
                            )
            except Exception:
                continue
        time.sleep(86400)

@bot.on_message(filters.command(['get_data']) & filters.private)
def get_data(client, message):
    if message:
        bot.send_message(message.chat.id,"Currently on Developing")
        return
    user_id = message.from_user.id
    chats = set()
    markup = types.InlineKeyboardMarkup(inline_keyboard=[])
    
    # Assuming you're using MongoDB as the database
    data = collection.find({'chat_id': {'$exists': True}})
    
    for dat in data:
        if 'chat_id' in dat:
            chat_id = dat['chat_id']
            if chat_id not in chats:
                chats.add(chat_id)
    
    # Retrieve chat information in parallel using threads
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        
        # Retrieve admins for each chat in parallel
        for chat_id in chats:
            futures.append(executor.submit(get_chat_admins, chat_id, user_id))
        
        # Process completed futures
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            
            if result is not None:
                chat_id, chat_title = result
                markup.inline_keyboard.append([types.InlineKeyboardButton(
                    f'{chat_title}', callback_data=f'data:{chat_id}:{user_id}')])

    text = "👉🏻 <u>Select the group</u> whose invite data you want to get.\n\n"
    text += "If a group in which you are an administrator doesn't appear here:\n • Either their is not a single invite data\n • Bot is not admin in that group"
    if chats != []:
        bot.send_message(message.chat.id, text, reply_markup=markup)
    else:
        bot.send_message(message.chat.id, text)

def get_chat_admins(chat_id, user_id):
    try:
        admins = bot.get_chat_members(chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS)
        for admin in admins:
            if admin.user.id == user_id:
                chat = bot.get_chat(chat_id)
                return chat_id, chat.title
    except Exception:
        return None
    
# time_threa = threading.Thread(target=delete_tracker)
# time_threa.start()

@bot.on_callback_query()
def callback_handler(client, callback_query):
    call = callback_query
    if call.data.startswith(("data:")):
        chat_id = int(call.data.split(":")[1])
        user_id = int(call.data.split(":")[2])
        try:
            data = collection.find({'chat_id': chat_id}).sort(
                "regular_count", -1)
            formatted_data = []
            serial_number = 1
            for da in data:
                # Extract the necessary data
                user_id = da['user_id']
                user = bot.get_chat_member(chat_id, user_id)
                total_invites_ = da['regular_count']
                regular_invites_ = da['total_count']
                left_invites_ = da['left_count']
                fake_invites_ = da['fake_count']
                username_ = user.user.username
                firstname_ = user.user.first_name

                # Format the data into a dictionary
                formatted_entry = {
                    'Serial No.': serial_number,
                    'Username': username_,
                    'First Name': firstname_,
                    'Total Invites': total_invites_,
                    'Regular Invites': regular_invites_,
                    'Fake Invites': fake_invites_,
                    'Left Invites': left_invites_
                }
                serial_number += 1
                # Append the formatted entry to the list
                formatted_data.append(formatted_entry)

            # Define the field names for the CSV file
            field_names = ['Serial No.', 'Username', 'First Name',
                           'Total Invites', 'Regular Invites', 'Fake Invites', 'Left Invites']
            chat = bot.get_chat(chat_id)
            # Generate the file name based on the chat title
            filename = 'invite-data.csv'

            # Write the formatted data to the CSV file
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=field_names)
                writer.writeheader()
                writer.writerows(formatted_data)

            # Send the CSV file to the user
            bot.send_document(user_id, filename)
            bot.send_message(user_id, f"Invite data for {chat.title}")
        except Exception as e:
            # Handle the exception
            error_message = str(e)
            print(e)
            # Inform the user about the error
            bot.send_message("@bnsl_boy", f"An error occurred while getting data {error_message}")
    elif call.data.startswith(("test:")):
        bot.answer_callback_query(call.id,"working on it")

@bot.on_message(filters.command(['role']))
def roles_given(client, message):
    chat_id = message.chat.id
    reply = message.reply_to_message
    if reply:
        user = reply.from_user.id
        user_name = reply.from_user.first_name
        role_name = message.text.split(" ")[1].lower()
        if role_name is None:
            bot.send_message(
                chat_id, "You did not provide me role name", reply_to_message_id=message.id)
            return

        find = roles.find_one(
            {'chat_id': chat_id, 'user_id': user, 'roles': role_name})
        if find:
            bot.send_message(
                chat_id, f"{user_name} already have {role_name} role", reply_to_message_id=message.id)
            return
        roles.update_one({'chat_id': chat_id, 'user_id': user},
                         {'$addToSet': {'roles': role_name},
                          '$set': {'first_name': user_name}},
                         upsert=True)
        bot.send_message(
            message.chat.id, f"{user_name} has been given the role of {role_name} in this chat")
    else:
        role_name = message.text.split(" ")[1].lower()
        if role_name is None:
            bot.send_message(
                chat_id, "You did not provide me role name", reply_to_message_id=message.id)
            return
        username = message.text.split(" ")[2:]
        if username is None:
            bot.send_message(chat_id, "You did not provide me users",
                             reply_to_message_id=message.id)
            return
        message_test = "User -  "
        for user in username:
            if not user.startswith("@"):
                for entity in message.entities:
                    if str(entity.type) == "MessageEntityType.TEXT_MENTION":
                        try:
                            name = entity.user.first_name
                            if name == user:
                                usser_id = entity.user.id
                                find = roles.find_one(
                                            {'chat_id': chat_id, 'user_id': usser_id, 'roles': role_name})
                                if find:
                                    bot.send_message(
                                        chat_id, f"{usser_name} already have {role_name} role", reply_to_message_id=message.id)
                                    continue

                                message_test += f"{user}, "
                                roles.update_one({'chat_id': chat_id, 'user_id': usser_id},
                                                {'$addToSet': {'roles': role_name},
                                                '$set': {'first_name': usser_name}}, upsert=True)
                        except Exception:
                            continue
                continue
            usser = bot.get_chat(user)
            usser_id = usser.id
            usser_name = usser.first_name

            find = roles.find_one(
                {'chat_id': chat_id, 'user_id': usser_id, 'roles': role_name})
            if find:
                bot.send_message(
                    chat_id, f"{usser_name} already have {role_name} role", reply_to_message_id=message.id)
                continue

            message_test += f"{user}, "
            roles.update_one({'chat_id': chat_id, 'user_id': usser_id},
                             {'$addToSet': {'roles': role_name},
                              '$set': {'first_name': usser_name}}, upsert=True)
        message_test += f"\n have been given the role of {role_name} in this chat"
        if message_test == "User -  \n have been given the role of ids in this chat":
            pass
        else:
            bot.send_message(chat_id,message_test)

score_board = {}

@bot.on_message(filters.dice)
def dice_handler(client, message):
    data = dices.find_one({'chat_id': message.chat.id, 'is_done': {'$exists': False}})
    if data:
        emoji = data['emoji']
        participants = data['participants']
        if emoji == "⚽️":
            emoji = "⚽"   
        if emoji == message.dice.emoji:
            user_id = str(message.from_user.id)
            value = message.dice.value
            chances = data['chances']
            if data['role'] is not None:
                role_name = data['role']
                data2 = roles.find_one({'chat_id': message.chat.id, 'roles': role_name})
                if data2 is None:
                    bot.send_message(message.chat.id, f"🚫 You need to have the {role_name} role to participate in this event.", reply_to_message_id=message.id)
                    return
            
            if user_id in participants and participants[user_id]['chances_used'] >= chances:
                bot.send_message(message.chat.id, "⚠️ You've used up all your chances.", reply_to_message_id=message.id)
                return

            
            if user_id in participants:
                participants[user_id]['chances_used'] += 1
            else:
                participants[user_id] = {'chances_used': 1, 'score': 0}

            participants[user_id]['first_name'] = message.from_user.first_name
            participants[user_id]['username'] = message.from_user.username
            participants[user_id]['score'] += value
            dices.update_one(
                {'chat_id': message.chat.id, 'is_done': {'$exists': False}},
                {'$set': {'participants': participants}}
            )
            if str(message.chat.id) not in score_board:
                score_board[str(message.chat.id)] = []
            if user_id not in score_board[str(message.chat.id)]:
                score_board[str(message.chat.id)].append(user_id)
            if len(score_board[str(message.chat.id)]) >= chances:
                send_score_board(message.chat.id)

def send_score_board(chat_id):
    user_ids = score_board[str(chat_id)]
    data = dices.find_one({'chat_id': chat_id, 'is_done': {'$exists': False}})
    
    message_text = "🎲 Score Update 🎲\n\n"
    if data:
        participants = data['participants']
        for user_id in user_ids:
            score = participants[user_id]['score']
            first_name = participants[user_id]['first_name']
            message_text += f"🔹 <a href='tg://user?id={user_id}'>{first_name}</a> - score : {score}\n"
    message_text += "\nUse /ranks to view the top 10 🏆"
    bot.send_message(chat_id, message_text)
    del score_board[str(chat_id)]

@bot.on_message(filters.command(['dices']))
def dice_handler(client, message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    is_admin = False
    is_how_to = False
    try:
        admins = bot.get_chat_members(chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS)
        for admin in admins:
            user_id2 = admin.user.id
            if user_id2 == user_id:
                is_admin = True
    except Exception as e:
        bot.send_message(chat_id, "Error in fetching group admin.")
        print("Error fetching admins:", e)
        return

    if not is_admin:
        bot.send_message(chat_id, "You must be an administrator to use this command.", reply_to_message_id=message.id)
        return

    args = message.text.split()[1:]
    emoji_list = ["🎲", "🎯", "🏀", "⚽️", "🎳"]

    duration_units = {"d": 86400, "h": 3600, "m": 60, "s": 1}
    if len(args) >= 4:
        try:
            emoji, chances, reward, duration = args[:4]
            chances = int(chances)
            reward = reward.replace("_", " ")
            duration = int(duration[:-1]) * duration_units[duration[-1]]
            role = None
        except (ValueError, KeyError, IndexError):
            bot.send_message(chat_id, "The command format is invalid. Usage: /dices <emoji> <chances> <Reward of Winners> <Duration>")
            return
        except Exception:
            bot.send_message(chat_id, "The command format is invalid. Usage: /dices <emoji> <chances> <Reward of Winners> <Duration>")
            return

        if emoji not in emoji_list:
            bot.send_message(chat_id, "Emoji not accepted. Try using one of these 🎲, 🎯, 🏀, ⚽️, 🎳")
            return

    if len(args) == 5:
        text = args[4]
        if text.startswith("role:"):
            role = text.split(":")[1]
            data = roles.find_one({'chat_id': chat_id, 'role_name': role})
            if data:
                if 'how_to_get' in data:
                    is_how_to = True
                    keyboard = types.InlineKeyboardMarkup(
                        [
                            [
                                types.InlineKeyboardButton(
                                    text=f'How to get {role}',
                                    callback_data=f"giveaway_how_to:{role}:{chat_id}"
                                )
                            ]
                        ]
                    )
                else:
                    bot.send_message(chat_id, f"{role} does not exist in this chat.", reply_to_message_id=message.id)
                    return

    dice_id = str(uuid.uuid4())
    time_left = duration
    time_left_str = f"{time_left // 86400}d:{(time_left % 86400) // 3600}h:{(time_left % 3600) // 60}m:{time_left % 60}s"

    document = {
        "dice_id": dice_id,
        "emoji": emoji,
        "chat_id": chat_id,
        "reward": reward,
        "chances": chances,
        "duration": duration,
        "role": role,
        "participants": {},
        "start_time": datetime.now(),
        "winners": [],
        "message_id": message.id + 1
    }
    dices.insert_one(document)

    message_text = f"🎉 Emoji Lucky Draw 🎉\n\n🍀 Participate in the lottery by sending the {emoji} emoji and earn points 🍀\n\n🎁 Reward - {reward} \n\n🏆 Chances - {chances} 🌟\n\n⏰ Ends in - {time_left_str} 🔥\n\n🎊 Achieve a high score & win big prizes! 🎁"

    if role:
        message_text += f"\n\n🌟 To participate in this Game , you need to have the {role} character"

    if is_how_to:
        bot.send_message(chat_id, message_text, reply_markup=keyboard)
    else:
        bot.send_message(chat_id, message_text)
    bot.send_dice(chat_id, emoji)
    try:
        bot.delete_messages(chat_id, message.id)
    except Exception:
        pass
    time_thread = threading.Thread(target=time_check)
    time_thread.start()

def end_dice(dice_id):
    dice = dices.find_one({'dice_id': dice_id})
    if dice:
        chat_id = dice["chat_id"]
        if dice["participants"] == {}:
            message_text = "No one participated in this game and this game has been cancelled. 🍀"
            dice_id2 = str(uuid.uuid4())
            dices.update_one({'dice_id': dice_id}, {'$set': {'dice_id': dice_id2, 'is_done': True}}, upsert=True)
            bot.send_message(chat_id, message_text)
            return

        sorted_participants = sorted(dice["participants"].items(), key=lambda x: x[1]['score'], reverse=True)
        max_chars_per_message = 500  # Telegram character limit for messages
        message_chunks = []
        current_chunk = ""

        current_chunk += "<b>The Game has ended 🍀</b><i>nleaderboard</i>\n\n"

        for i, (user_id, score) in enumerate(sorted_participants):
            first_name = score['first_name']
            if i == 0:
                current_chunk += f"🥇 - <a href='tg://user?id={user_id}'>{first_name}</a> - {score['score']}\n"
            elif i == 1:
                current_chunk += f"🥈 - <a href='tg://user?id={user_id}'>{first_name}</a> - {score['score']}\n"
            elif i == 2:
                current_chunk += f"🥉 - <a href='tg://user?id={user_id}'>{first_name}</a> - {score['score']}\n"
            else:
                current_chunk += f"🏅 - <a href='tg://user?id={user_id}'>{first_name}</a> - {score['score']}\n"

            if len(current_chunk) >= max_chars_per_message:
                message_chunks.append(current_chunk)
                current_chunk = ""

        if current_chunk:
            message_chunks.append(current_chunk)

        for chunk in message_chunks:
            bot.send_message(chat_id, chunk)
        dice_id2 = str(uuid.uuid4())
        dices.update_one({'dice_id': dice_id}, {'$set': {'dice_id': dice_id2, 'is_done': True}}, upsert=True)
       
@bot.on_message(filters.command(['ranks']))
def ranks_sender(client,message):
    data = dices.find_one({'chat_id': message.chat.id, 'is_done': {'$exists': False}})
    if data:
        if data["participants"] == {}:
            message_text = "No users are involved."
            bot.send_message(message.chat.id, message_text)
            return

        sorted_participants = sorted(data["participants"].items(), key=lambda x: x[1]['score'], reverse=True)

        current_chunk = "🏆 Top 10 Leaderboard - \n\n"

        for i, (user_id, score) in enumerate(sorted_participants):
            first_name = score['first_name']
            if i == 0:
                current_chunk += f"🥇 - <a href='tg://user?id={user_id}'>{first_name}</a> - {score['score']}\n"
            elif i == 1:
                current_chunk += f"🥈 - <a href='tg://user?id={user_id}'>{first_name}</a> - {score['score']}\n"
            elif i == 2:
                current_chunk += f"🥉 - <a href='tg://user?id={user_id}'>{first_name}</a> - {score['score']}\n"
            else:
                current_chunk += f"🏅 - <a href='tg://user?id={user_id}'>{first_name}</a> - {score['score']}\n"
            
            if i == 9:
                break
    
        bot.send_message(message.chat.id, current_chunk)
    else:
        bot.send_message(message.chat.id, "No ongoing giveaway found.")

lock = threading.Lock()

def time_check():
    with lock:
        time.sleep(10)
        while True:
            dicess = dices.find()
            i = 1
            for giveaway in dicess:
                if 'is_done' in giveaway:
                    continue
                giveaway["duration"] -= 10
                time_left = giveaway["duration"]
                dice_id = giveaway['dice_id']
                i += 1
                dices.update_one({'dice_id': dice_id}, {'$set': {'duration': giveaway["duration"]}}) 
                if time_left <= 0:
                    end_dice(dice_id)
            if i == 1:
                return False
            time.sleep(10)

time_thread = threading.Thread(target=time_check)
time_thread.start()

@bot.on_message(filters.command(['twisend']))
def twitter_send(client,message):
    try:
        chat_ids = persons['twitter']
        if message.reply_to_message :
            if message.reply_to_message.photo:
                file_id = message.reply_to_message.photo.file_id
                caption = message.reply_to_message.caption.html
                if message.reply_to_message.reply_markup:
                    markup = message.reply_to_message.reply_markup
                    for chat_id in chat_ids:
                        try:
                            send_photo = bot.send_photo(chat_id, file_id, caption=caption, reply_markup=markup)
                            bot.pin_chat_message(send_photo.chat.id, send_photo.id, True)
                            bot.delete_messages(send_photo.chat.id, send_photo.id+1)
                        except Exception as e:
                            continue
                else:
                    for chat_id in chat_ids:
                        try:
                            send_photo = bot.send_photo(chat_id, file_id, caption=caption)
                            bot.pin_chat_message(send_photo.chat.id, send_photo.id, True)
                            bot.delete_messages(send_photo.chat.id, send_photo.id+1)
                        except Exception as e:
                            continue
            else:
                text = message.reply_to_message.text.html
                if message.reply_to_message.reply_markup:
                    markup = message.reply_to_message.reply_markup
                    for chat_id in chat_ids:
                        try:
                            send_message = bot.send_message(chat_id, text, disable_web_page_preview=True, reply_markup=markup)
                            bot.pin_chat_message(send_message.chat.id, send_message.id)
                            bot.delete_messages(send_message.chat.id, send_message.id+1)
                        except Exception as e:
                            continue
                else:
                    for chat_id in chat_ids:
                        try:
                            send_message = bot.send_message(chat_id, text, disable_web_page_preview=True)
                            bot.pin_chat_message(send_message.chat.id, send_message.id)
                            bot.delete_messages(send_message.chat.id, send_message.id+1)
                        except Exception as e:
                            continue

    except Exception as e :
        bot.send_message(1443989714,f"{e}")
        print(e)


@bot.on_message(filters.command(['me']) & filters.group)
def me_check(client, message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    data = roles.find_one({'user_id': user_id, 'chat_id': chat_id})

    if data:
        messagetext = "Current you have following Roles :-"
        rolees = data['roles']
        for role in rolees:
            messagetext += f"\n • {role}"
        bot.send_message(chat_id, messagetext)
    else:
        messagetext = "Current you have following Roles :-"
        bot.send_message(chat_id, messagetext)

bot.run()
