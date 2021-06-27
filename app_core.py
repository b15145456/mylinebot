# 載入需要的模組
from __future__ import unicode_literals
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError

app = Flask(__name__)

# LINE 聊天機器人的基本資料
line_bot_api = LineBotApi('hYPuOASu+QuF4+a8pHDKnJfOkHTlJWqzODsGmVTUHj9QCZ/OcByDSYsa53q4f6/WvF2/L4WqUS1xh9wZwvLpLkhwf7C1409ST36yb/wvS2mCctGzQEVXp8h/DSxhAXPzGcqzLNgqNuLJoNtMmRkKbwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('9d3025704247348be7d2ad1dc0079b21')

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

if __name__ == "__main__":
    app.run()