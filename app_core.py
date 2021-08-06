from __future__ import unicode_literals
import os
import json
# 增加了 render_template
from flask import Flask, request, abort, render_template

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, FlexSendMessage

import configparser

import urllib
import re
import random
# try git on vs code   
from custom_models import prepare_record, line_insert_record, show_records, utils

app = Flask(__name__)

# LINE 聊天機器人的基本資料
config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))

@app.route("/")
def home():
    return render_template("home.html")

# @app.route("/from_start")
# def from_start():
#     return render_template("from_start.html")

# @app.route("/show_records")
# def show():
#     python_records = show_records.web_select_overall()
#     return render_template("show_records.html", html_records=python_records)

@app.route("/submit", methods=['POST'])
def submit():
    change_num = int(request.values['change_num'])
    utils.edit_number(change_num)
    nowNumFromDB = utils.get_number()
    tokensListFromDB = utils.get_tokenList()
    nowNum = nowNumFromDB[0]
    return render_template('clinic_page.html', now_num_records = nowNum, token_list = tokensListFromDB)


# @app.route("/changeNumTo/<n>")    
# def webhchangeNum(n):
#     if n.isnumeric():
#         data = ["0",str(n)]
#         utils.edit_number(data)
#     return render_template('clinic_page.html', html_records = data)

# @app.route("/submit", methods=['POST'])
# def submit():
#     new_num = request.values['change_num']
#     data = [0,new_num]
#     utils.edit_number(data)
#     data = utils.get_number()
#     return render_template('clinic_page.html', html_records = data)

@app.route("/clinic_number")    
def show_clinic_num():
    dataFromDB = utils.get_number()
    nowNumFromDB = utils.get_number()
    tokensListFromDB = utils.get_tokenList()
    nowNum = nowNumFromDB[0]
    return render_template('clinic_page.html', now_num_records = nowNum, token_list = tokensListFromDB)

# 增加的這段放在上面

# 接收 LINE 的資訊
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# 請 pixabay 幫我們找圖
@handler.add(MessageEvent, message=TextMessage)
def pixabay_isch(event):
    if 'token' in event.message.text:
        line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=str(event))
            )
    elif 'change' in event.message.text:  # 0 change to 5
        try:
            data_list = event.message.text.split(" ")   # data_list = [0, change, to, 5]
            reply = utils.edit_number(data_list[3])
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=reply)
            )
            
        except:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='失敗了')
            )

    elif '草泥馬訓練紀錄' in event.message.text:
        try:
            record_list = prepare_record.prepare_record(event.message.text)
            reply = line_insert_record.line_insert_record(record_list)

            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=reply)
            )
                
        except:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='失敗了')
            )
    elif '選單' in event.message.text:
        f = open('./flex_message/menu.json',)
        data = json.load(f)
        line_bot_api.reply_message(
                    event.reply_token,
                    FlexSendMessage(
                        alt_text = 'index',
                        contents = data
                    )
                )
    else:
        try:
            我想找圖 = {'q': event.message.text}
            url = f"https://imgur.com/search?{urllib.parse.urlencode(我想找圖)}/"
            hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                'Accept-Encoding': 'none',
                'Accept-Language': 'en-US,en;q=0.8',
                'Connection': 'keep-alive'}  

            req = urllib.request.Request(url, headers = hdr)
            conn = urllib.request.urlopen(req)

            print('fetch page finish')

            pattern = 'src="\S*.jpg"'
            img_list = []

            for match in re.finditer(pattern, str(conn.read())):
                img_list.append(match.group()[14:-1])

            print(img_list)

            random_img_url = 'https://i.imgur'+img_list[random.randint(0, len(img_list)+1)]
            print('fetch img url finish')
            print(random_img_url)

            line_bot_api.reply_message(
                event.reply_token,
                ImageSendMessage(
                    original_content_url=random_img_url,
                    preview_image_url=random_img_url
                )
            )
        # 如果找不到圖，就學你說話
        except:
            print('cannot find phote')
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text = "Hey!" + str(event.source.user_id) +"\n I can't understand your request!")
            )
            pass
if __name__ == "__main__":
    app.run()