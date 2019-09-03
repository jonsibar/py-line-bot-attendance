import os
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
import attendance

app = Flask(__name__)

line_bot_api = LineBotApi('MoEx8xr4EwfVkocXBaBQmWb9DOoVlgN2XG/LrI4aOrWxW294jb26W5w3+t+0d+sFsNixnXqtHkmLbI0nF6nxWPtCTjbWOAe4ZMKJJZXocuzrd+pD2bkBtw4WplL16tpY9wcB651F3j10w/Y+1YR7JwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('aaba13e6dd0d3e30113f14e73ccd9a41')


@app.route("/callback", methods=['POST'])
def callback():
    # Get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # Get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # Handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    """ Here's all the messages will be handled and processed by the program """
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=attendance.attendance))

    if text == 'absen':
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=attendance.attendance))

        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="ngomong ape lur"))

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)