# 載入需要的模組
from __future__ import unicode_literals
import os
import psycopg2
from flask import Flask, request, abort, render_template, redirect, jsonify
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage


# try pull request！

import configparser

from models import botTalk, callDatabase

app = Flask(__name__)

# LINE 聊天機器人的基本資料
config = configparser.ConfigParser()
config.read('config.ini')

handler = WebhookHandler(config.get('line-bot', 'channel_secret'))

# 首頁
@app.route("/")
def home():
    clinic1 = callDatabase.getClinicNum(1)[0]
    clinic2 = callDatabase.getClinicNum(2)[0]
    list1 = callDatabase.getIdListFromClinic(1)
    list2 = callDatabase.getIdListFromClinic(2)

    if clinic1 == False:
        clinic1 = (None,)
    if clinic2 == False:
        clinic2 = (None,)
    if list1 == False:
        list1 = [(None,None)]
    if list2 == False:
        list2 = [(None,None)]

    print('--------------------------{} : {} : {} : {}--------------------------'.format(clinic1, clinic2, list1, list2))
    return render_template('home.html', clinic_info_1 = clinic1, clinic_info_2 = clinic2, id_list_1 = list1, id_list_2 = list2)

@app.route("/submit", methods=['POST'])
def submit():
    change_num = int(request.values['change_num'])
    callDatabase.updateClinicNum(1, change_num)
    botTalk.checkNum(1)
    return redirect("/")

# test page
@app.route("/test")
def test():
    list = callDatabase.getIdList()
    return render_template('test.html', id_list = list)

# test function zzz
@app.route("/function2", methods=['POST'])
def addNum():
    num = callDatabase.getClinicNum(2)[0][0] + 1
    callDatabase.updateClinicNum(2, num)
    botTalk.checkNum(2)
    return redirect("/")

@app.route("/function3", methods=['POST'])
def resetNum():
    callDatabase.updateClinicNum(2, 0)
    return redirect("/")

#test Ajax zzzz
@app.route("/reset", methods=['GET','POST'])
def reset(clinic_id):
    print('---------------request.data------------------------------------------')
    print(request.get_json())
    if request.method == 'POST':
        try:
            callDatabase.updateClinicNum(request.data, 0)
            result = {'success': True, 'response': 'reset clinic number'}
        except:
            result = {'success': False, 'response': 'Something went wrong'}
        return jsonify(result)
    else:
        return render_template('home.html')
    



# 接收 LINE 的資訊
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    print("-----------------------------body-----------------------------")
    print(body)
    print("---------------------------body end---------------------------")

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# 當收到 LINE 的 MessageEvent (信息事件)，而且信息是屬於 TextMessage (文字信息) 時就執行
@handler.add(MessageEvent, message=TextMessage)
def reply_text_message(event):
    reply = False

    if not reply:
        reply = botTalk.adminCmd(event)

    if not reply:
        reply = botTalk.lineId(event)

    if not reply:
        reply = botTalk.deleteId(event)

    if not reply:
        reply = botTalk.reply(event)

if __name__ == "__main__":
    app.run()
