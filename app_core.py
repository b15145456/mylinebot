from __future__ import unicode_literals
import os
import json
# 增加了 render_template
from flask import Flask, request, abort, render_template, redirect
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, FlexSendMessage
from flask_socketio import SocketIO, emit
import configparser
import urllib
import re
import random
# try git on vs code   
from custom_models import utils
app = Flask(__name__)
# LINE 聊天機器人的基本資料
config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/submit", methods=['POST'])
def submit():
    change_num = int(request.values['change_num'])
    utils.edit_number(change_num)
    utils.del_token_data(change_num)
    return redirect("/clinic_number")


@app.route("/clinic_number")    
def show_clinic_num():
    dataFromDB = utils.get_number()
    data = dataFromDB[0]
    return render_template("clinic_page.html", html_records = data)
# socketio = SocketIO(app)

# @socketio.on('connect_event')
# def connected_msg(msg):
#     emit('server_response', {'data': msg['data']})

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
    if (event.message.text.isdigit()):
        insert_data = [event.source.user_id, int(event.message.text)]
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
    # socketio.run(app)