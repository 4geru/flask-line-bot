# coding: UTF-8

from dotenv import load_dotenv
from os.path import join, dirname
import os

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

load_dotenv(join(dirname(__file__), '../.env'))

line_bot_api = LineBotApi(os.environ['LINE_CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['LINE_CHANNEL_SECRET'])

def return_message(event):
    print(event)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

def handle(body, signature):
    print('call')
    handler.handle(body, signature)
