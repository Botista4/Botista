import time
import telebot
from instagrapi import Client
from datetime import datetime
from server import server

API_KEY = '6262533922:AAF6R3TIjcvBU_oo_wMoMgokFf7d60uLXig'
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
                bot.send_chat_action(message.chat.id, 'upload_photo')
                m = message.text.replace("/pfp @", "")
                x = cl.user_info_by_username(m)
                url = x.profile_pic_url_hd
                caption = "Name: " + x.full_name + "\nUsername: " + m + "\nBio:\n" + x.biography
                bot.send_photo(message.chat.id, url, caption, reply_to_message_id=message.message_id)
            except:
                bot.reply_to(message, "Unvalid username.")
        chat(message)

    @bot.message_handler(func=lambda m: True)
    def get_media(message):
        delete = bot.reply_to(message, 'Processing...')
        m = message.text
        try: 
            x = cl.media_pk_from_url(m)
            minfo = cl.media_info(x)
            info = minfo.product_type
            media = minfo.media_type
            likes = "Likes: " + f'{minfo.like_count:,}'
            caption = minfo.caption_text + "\n\n" + likes
        except:
            info = None
            media = None
            bot.delete_message(message.chat.id, delete.message_id, timeout=10)
            bot.reply_to(message, "Unvalid, plesae send a public Instgram link.")

        chat(message)

        if info == "clips":
            clip_url = cl.media_info(x).video_url
            bot.delete_message(message.chat.id, delete.message_id, timeout=10)
            bot.send_chat_action(message.chat.id, action='upload_video')
            bot.send_video(chat_id=message.chat.id, video=clip_url, timeout=200, caption=caption, reply_to_message_id=message.message_id)

        if info == "igtv":
            tvurl = cl.media_info(x).video_url
            bot.delete_message(message.chat.id, delete.message_id, timeout=10)
            bot.send_chat_action(message.chat.id, action='upload_video')
            bot.send_video(chat_id=message.chat.id, video=tvurl, timeout=200, caption=caption, reply_to_message_id=message.message_id)

        if media == 1:
            thumbnail = minfo.thumbnail_url
            bot.delete_message(message.chat.id, delete.message_id, timeout=10)
            bot.send_chat_action(message.chat.id, action='upload_photo')
            bot.send_photo(chat_id=message.chat.id, photo=thumbnail, timeout=200, caption=caption, reply_to_message_id=message.message_id)

        if media == 8:
            bot.delete_message(message.chat.id, delete.message_id, timeout=10)
            bot.reply_to(message, text=caption)
            for f in range(len(minfo.resources)):
                index = minfo.resources[f]
                mtype = index.media_type
                if mtype == 1:
                    bot.send_chat_action(message.chat.id, action='upload_photo')
                    bot.send_photo(message.chat.id, index.thumbnail_url)
                if mtype == 2:
                    bot.send_chat_action(message.chat.id, action='upload_video')
                    bot.send_video(message.chat.id, index.video_url)

    print('Bot is running...')
    while True:
        try:
            bot.infinity_polling()
        except Exception as ex:
            print("Error:\n")
            print(ex)
            time.sleep(10)
            bot.infinity_polling()

if __name__ == "__main__":
    tbot()
