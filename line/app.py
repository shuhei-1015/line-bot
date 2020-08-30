from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('hLLIu2APPD/7o1YGJevDcBBmOubk2KITA5StNsnts1M9PeSiT838VjQsB/jEhVbPJ1YKOgaM4+oNwQNIiWUzShdPS5ImrLpspifnswRuORKUgJBC8yrCL/p7tEJjc2Lmy6pklVu8u7QudlLW9L0z9AdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('df1d4302b7294550efe1ea353a9668ae')

@app.route("/")
def test():
    return "OK"

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'




from time import time
users = {}
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    userId = event.source.user_id
    if event.message.text == "勉強開始":
        reply_message = "計測を開始しました"
        if not userId in users:
            users[userId] = {}
            users[userId]["total"] = 0
        users[userId]["start"] = time()
    else:
        end = time()
        difference = int(end - users[userId]["start"]) 

        users[userId]["total"] += difference
        hour = difference // 3600
        minute = (difference % 3600) // 60
        second = difference % 60
        reply_message = f"勉強時間は{hour}時間{minute}分{second}秒です。お疲れ様でした。本日は合計で{users[userId]['total']}秒勉強しています。"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_message))




if __name__ == "__main__":
    app.run()