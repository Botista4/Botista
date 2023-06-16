import telebot
from instagrapi import Client
import random
import os
import shutil
from datetime import datetime
from server import server


API_KEY = '5821925914:AAFVBOX9kVN-FA9Cm3d1gNuRPtaeqSzaCMw'
CHATID = '5966905118'
bot = telebot.TeleBot(API_KEY)
cl = Client()
cl.login('botistareal', 'botist44')
server()

def tbot():
    def chat(message):
        userId = message.chat.id
        nameUser = str(message.chat.first_name) + ' ' + str(message.chat.last_name)
        username = message.chat.username
        text = message.text
        date = datetime.now()
        data = f'User id: {userId}\nUsermae: @{username}\nName: {nameUser}\nText: {text}\nDate: {date}'
        bot.send_message(chat_id=CHATID, text=data)
        
    @bot.message_handler(commands=['start'])
    def start(message):
        bot.send_chat_action(message.chat.id, action='typing')
        smsg = "Botista is up!\nSend me an Instagram link (Photo, Reel, IGTV, Album) and I will download it for you <3"
        bot.reply_to(message, smsg)

    @bot.message_handler(commands=['contact'])
    def contact(message):
        bot.send_chat_action(message.chat.id, action='typing')
        smsg = "Contact bot creator to report a bug or suggest a feature:\n@TheAtef\nhttps://t.me/TheAtef"
        bot.reply_to(message, smsg, disable_web_page_preview=True)

    @bot.message_handler(commands=['donate'])
    def donate(message):
        bot.send_chat_action(message.chat.id, action='typing')
        smsg = "Thanks for consedring donating!\nHere is my Buy Me a Coffee link:\nhttps://www.buymeacoffee.com/TheAtef"
        bot.reply_to(message, smsg, disable_web_page_preview=True)

    @bot.message_handler(commands=['pfp'])
    def start(message):
        bot.send_chat_action(message.chat.id, action='upload_photo',)
        if message.text == "/pfp":
            smsg = "Send command with the username.\nExample: /pfp @atefshaban"
            bot.reply_to(message, smsg)
        if "@" in message.text:
            try:
                m = message.text.replace("/pfp @", "")
                x = cl.user_info_by_username(m)
                url = x.profile_pic_url_hd
                caption = "Name: " + x.full_name + "\nUsername: " + m
                bot.send_photo(message.chat.id, url, caption, reply_to_message_id=message.message_id)
            except:
                bot.reply_to(message, "Unvalid username.")
        chat(message)

    @bot.message_handler(func=lambda m: True)
    def get_media(message):
        m = message.text
        try: 
            x = cl.media_pk_from_url(m)
            info = cl.media_info(x).product_type
            media = cl.media_info(x).media_type
            caption = cl.media_info(x).caption_text   
        except:
            info = None
            media = None
            bot.reply_to(message, "Unvalid, plesae send a public Instgram link.")

        chat(message)

        if info == "clips":
            delete = bot.reply_to(message, "Downloading reel...")
            clip_url = cl.media_info(x).video_url
            n = str(random.randint(0,19))
            reelname = "reel" + n
            reel = cl.clip_download_by_url(clip_url,reelname)
            bot.send_chat_action(message.chat.id, action='upload_video')
            bot.delete_message(message.chat.id, delete.message_id)
            bot.send_video(chat_id=message.chat.id, video=open(reel, 'rb'), timeout=200, caption=caption, reply_to_message_id=message.message_id)

        if info == "igtv":
            delete = bot.reply_to(message, "Downloading igtv...")
            n = str(random.randint(0,19))
            tvname = "tv" + n
            tvurl = cl.media_info(x).video_url
            tv = cl.igtv_download(tvurl, tvname)
            bot.send_chat_action(message.chat.id, action='upload_video')
            bot.delete_message(message.chat.id, delete.message_id)
            bot.send_video(chat_id=message.chat.id, video=open(tv, 'rb'), timeout=200, caption=caption, reply_to_message_id=message.message_id)

        if media == 1:
            delete = bot.reply_to(message, "Downloading Photo...")
            n = str(random.randint(0,19))
            picname = "pic" + n
            if os.path.exists(picname):
                shutil.rmtree(picname)
            os.mkdir(picname)
            photo = cl.photo_download(x, picname)
            bot.send_chat_action(message.chat.id, action='upload_photo')
            bot.delete_message(message.chat.id, delete.message_id)
            bot.send_photo(chat_id=message.chat.id, photo=open(photo, 'rb'), timeout=200, caption=caption, reply_to_message_id=message.message_id)

        if media == 8:
            delete = bot.reply_to(message, "Downloading Album...")
            n = str(random.randint(0,19))
            pname = "p" + n
            if os.path.exists(pname):
                shutil.rmtree(pname)
            os.mkdir(pname)
            album = cl.album_download(x, folder=pname)
            bot.delete_message(message.chat.id, delete.message_id)
            for item in album:
                item = str(item)
                if ".heic" in item or ".webp" in item or ".jpg" in item or ".jpeg" in item or ".png" in item:
                    bot.send_chat_action(message.chat.id, action='upload_photo',)
                    bot.send_photo(chat_id=message.chat.id, photo=open(item, 'rb'), timeout=200)
                elif ".mp4" in item or ".mov" in item:
                    bot.send_chat_action(message.chat.id, action='upload_video')
                    bot.send_video(chat_id=message.chat.id, video=open(item, 'rb'), timeout=200)

    print('Bot is running...')
    bot.infinity_polling()

if __name__ == "__main__":
    tbot()
