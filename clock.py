from apscheduler.schedulers.blocking import BlockingScheduler
# from linebot import LineBotApi, WebhookHandler
# from linebot.models import MessageEvent, TextMessage, TextSendMessage


import urllib
import urllib.request
import datetime
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

# line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
# handler = WebhookHandler(config.get('line-bot', 'channel_secret'))

sched = BlockingScheduler()

@sched.scheduled_job('cron', hour='8-22', minute='*/20')
def scheduled_job():
    url = "https://clinic-bot-v1.herokuapp.com/"
    conn = urllib.request.urlopen(url)
        
    for key, value in conn.getheaders():
        print(key, value)

    # line_bot_api.push_message('U5bdce5ac2205e9325e1a05fdd32f9677', TextSendMessage(text='20分鐘惹'))

sched.start()