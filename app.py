# coding: UTF-8
import os
import sys
import ast
from os.path import join, dirname
from flask import Flask, request, abort
from dotenv import load_dotenv
from linebot import LineBotApi
from linebot.exceptions import LineBotApiError


from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
)

load_dotenv(join(dirname(__file__), '.env'))


app = Flask(__name__)

# 環境変数からchannel_secret・channel_access_tokenを取得
channel_secret = os.environ['LINE_CHANNEL_SECRET']
channel_access_token = os.environ['LINE_CHANNEL_ACCESS_TOKEN']

if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

@app.route("/")
def hello_world():
    return "hello world!"

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
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    body = request.get_data(as_text=True)
    data = ast.literal_eval(body)
    data = data["events"][0] 
    # app.logger.info(data)
    try:
        profile = line_bot_api.get_profile(data['source']['userId'])
        print(profile.display_name)
        print(profile.user_id)
        print(profile.picture_url)
        
        # line_bot_api.reply_message(
        #     event.reply_token,
        #     ImageSendMessage(
        #         original_content_url="https://res.cloudinary.com/dzhcf23xd/image/upload/v1503874903/pf7u56fr8qoqtl6pfhph.jpg",
        #         preview_image_url="https://res.cloudinary.com/dzhcf23xd/image/upload/v1503874903/pf7u56fr8qoqtl6pfhph.jpg",
        # ))
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text))
    except LineBotApiError as e:
        app.logger.info(e)
    

if __name__ == "__main__":
    app.run(host=os.getenv("IP", '0.0.0.0'), port=int(os.getenv("PORT", 8080)))
    # app.run()