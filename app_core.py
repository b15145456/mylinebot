from __future__ import unicode_literals
import os
import json
# 增加了 render_template
from flask import Flask, request, abort, render_template

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, FlexSendMessage
from flask_socketio import SocketIO, emit
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

socketio = SocketIO(app)

@socketio.on('connect_event')
def connected_msg(msg):
    emit('server_response', {'data': msg['data']})

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

""" Json format from line
{
  "message": {
    "id": "14523548164652",
    "text": "token",
    "type": "text"
  },
  "replyToken": "ade42d67c8644e409b83fce165687b46",     replyToken -> reply_token
  "source": {
    "type": "user",
    "userId": "Uc20f5abc2ef473849e0958ba31a42044"       userId -> user_id
  },                
  "timestamp": 1628220861293,
  "type": "message"

}"""

# 請 pixabay 幫我們找圖
@handler.add(MessageEvent, message=TextMessage)
def pixabay_isch(event):
    if (event.message.text.isdigit()):
        insert_data = [event.source.user_id, int(event.message.text), event.reply_token]
        if utils.exit_token(insert_data):
            res = utils.change_token_data(insert_data)
        else:
            res = utils.insert_token(insert_data)
        line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text = res)
            )
        
    elif 'token' in event.message.text:
        line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text = str(event))
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
    socketio.run(app)