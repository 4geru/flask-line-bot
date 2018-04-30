from dotenv import load_dotenv
from os.path import join, dirname
import os
from flask import Flask, request, abort
from linebot.exceptions import LineBotApiError
import line.line as line
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
from linebot.exceptions import (
    InvalidSignatureError
)
load_dotenv(join(dirname(__file__), '.env'))

app = Flask(__name__)

# channel_secret = os.environ['LINE_CHANNEL_SECRET']
# channel_access_token = os.environ['LINE_CHANNEL_ACCESS_TOKEN']

line_bot_api = LineBotApi(os.environ['LINE_CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['LINE_CHANNEL_SECRET'])

# @handler.add(MessageEvent, message=TextMessage)
# def handle_message(event):
#     line_bot_api.reply_message(
#         event.reply_token,
#         TextSendMessage(text=event.message.text))

# def handle(body, signature):
#     handler.handle(body, signature)

@app.route("/")
def hello_world():
    return "hello world!"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line.return_message(event)

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        print("success")
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("invalid")
        abort(400)

    return "OK"
 

if __name__ == "__main__":
    app.run(host=os.getenv("IP", '0.0.0.0'), port=int(os.getenv("PORT", 8080)))