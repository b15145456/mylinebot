from __future__ import unicode_literals
import os

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, PostbackEvent, TextMessage, TextSendMessage, ImageSendMessage, FlexSendMessage

import configparser

from models import callDatabase

# LINE 聊天機器人的基本資料
config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
admin_id = 'Uc20f5abc2ef473849e0958ba31a42044'

def checkNum(clinic):

    num = callDatabase.getClinicNum(clinic)[0][0]
    list = callDatabase.getIdListFromClinic(clinic)

    for i in list:

        if i[1] - num == 5:
            line_bot_api.push_message(i[0], TextSendMessage(text='再 {} 個人就到您了，別走太遠唷😥'.format(i[1] - num)))
        elif i[1] - num == 2:
            line_bot_api.push_message(i[0], TextSendMessage(text='再 {} 位就是您！請在現場等候，以免過號唷😉'.format(i[1] - num)))

        # if 1 <= i[1] - num <= 5:
        #     line_bot_api.push_message(i[0], TextSendMessage(text='再 {} 個人就到您了，別走太遠唷😥'.format(i[1] - num)))

        elif i[1] - num == 0:
            # line_bot_api.push_message(i[0], TextSendMessage(text='輪到你ㄌ {}'.format(i[0])))
            callDatabase.deleteIdUseNum(num)

def adminCmd(event):

    if event.source.user_id == admin_id:

        if event.message.text == "/+1":
            num = 0

            if callDatabase.getClinicNum(1):
                num = callDatabase.getClinicNum(1)[0][0]
                num += 1
                callDatabase.updateClinicNum(1,num)
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text='診間 1 現在看到' + str(num))
                ) 
            else:
                callDatabase.addClinicNum(1,num)
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text='init clinic 1 number to 0')
                )
            checkNum(1)
            return True

        if event.message.text == "/+1_2":
            num = 0

            if callDatabase.getClinicNum(2):
                num = callDatabase.getClinicNum(2)[0][0]
                num += 1
                callDatabase.updateClinicNum(2,num)
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text='診間 2 現在看到' + str(num))
                ) 
            else:
                callDatabase.addClinicNum(2,num)
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text='init clinic 2 number to 0')
                )
            checkNum(2)
            return True
        
        if event.message.text == "/list":
            list = str(callDatabase.getIdList())
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=list)
            )
            return True
        
        if event.message.text == "/list1":
            list = str(callDatabase.getIdListFromClinic(1))
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=list)
            )
            return True

        if event.message.text == "/list2":
            list = str(callDatabase.getIdListFromClinic(2))
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=list)
            )
            return True

        if event.message.text == "/initTable":
            callDatabase.initTable()
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='init table successfully')
            )
            return True

        if event.message.text == "/addId":
            callDatabase.addLineId('TestID000000000000000000000000001', 1, 100)
            callDatabase.addLineId('TestID000000000000000000000000002', 1, 101)
            callDatabase.addLineId('TestID000000000000000000000000003', 2, 200)
            callDatabase.addLineId('TestID000000000000000000000000004', 2, 201)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='add some line id successfully')
            )
            return True

        if event.message.text == "/test":
            data1 = str(callDatabase.getIdNum(admin_id)[0][0])
            data2 = str(callDatabase.getIdNum(admin_id)[0][1])
            data3 = str(callDatabase.getIdNum(admin_id)[0][2])
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='{} {} {}'.format(data1, data2, data3))
            )
            return True
    else:
        return False

def lineId(event):

    line_id = event.source.user_id
    clinic = 0

    if event.message.text.isdecimal():

        num = int(event.message.text)
        idNum = callDatabase.getIdNum(line_id)

        if idNum:
            if idNum[0][2] == 0:
                callDatabase.updateLineNum(line_id, num)
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text='成功登記提醒號為 {} 🌝。\n💡請注意：僅於「倒數5位」與「倒數2位」提醒❗️'.format(num))
                )
            elif idNum[0][2] > 0:
                callDatabase.updateLineNum(line_id, num)
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text='已更新提醒號為 {}。\n💡請注意：僅於「倒數5位」與「倒數2位」提醒❗️'.format(num))
                )  
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='請先選擇診間')
            )
        return True

    elif ('診間' in event.message.text):

        str1 = event.message.text.split(' ')
        clinic = int(str1[1])

        if callDatabase.getIdNum(line_id):
            callDatabase.updateLineClinic(line_id, clinic)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='已更新為診間{}'.format(clinic))
            )
        else:
            callDatabase.addLineId(line_id, clinic, 0)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='成功登記診間{}'.format(clinic))
            )
        return True
    else: 
        return False

def deleteId(event):

    if event.message.text == '取消提醒':
        callDatabase.deleteIdUseId(event.source.user_id)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='已成功取消提醒')
        )
        return True
    else:
        return False

def reply(event):

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=str(event))
    )
    return True