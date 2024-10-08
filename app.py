import os
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    LineBotApiError, InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, DatetimePickerAction,
    CameraAction, CameraRollAction, LocationAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    MemberJoinedEvent, MemberLeftEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, SpacerComponent, IconComponent, ButtonComponent,
    SeparatorComponent, QuickReply, QuickReplyButton,
    ImageSendMessage)
from dotenv import load_dotenv
import scrape
import login


app = Flask(__name__)

load_dotenv()

line_bot_api = LineBotApi('LINE_CHANNEL_ACCESS_TOKEN')
handler = WebhookHandler('LINE_CHANNEL_SECRET')


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




@handler.add(FollowEvent)
def handle_follow(event):
	profile = line_bot_api.get_profile(event.source.user_id)
	line_bot_api.reply_message(
			event.reply_token,
			TextSendMessage(text='Hai, ' + profile.display_name + '\nSaya Budi, budak digital yang siap membantu keperluan bolosmu :D\nSilahkan ketik /perintah jika kamu bingung')
			)

@handler.add(JoinEvent)
def handle_join(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='Hai gais '+ '\nSaya Budi, budak digital yang siap membantu keperluan bolosmu :D\nSilahkan ketik /perintah jika kamu bingung'
            )
        )


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text.lower()
    commands = ['/absen', '/jatah', '/elearning', '/ujian', '/user']
    names = names(login)
    for command in commands:
        if command in text.split():
            for name in names:
                if name in text.split():
                    if command == '/absen':
                        scrape.presensi(getattr(login,name))
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text=scrape.attendance)
                            )
                    elif command == '/jatah':
                        scrape.bolos(getattr(login,name))
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text=scrape.absen_list)
                            )
                    elif command == '/elearning':
                        scrape.mats(getattr(login,name))
                        if hasattr(event.source, 'group_id'):
                            for pushmsg in scrape.elearning_list:
                                line_bot_api.push_message(
                                    event.source.group_id, [
                                    TextSendMessage(text=pushmsg),
                                    ]
                                    )
                        else:
                             for pushmsg in scrape.elearning_list:
                                line_bot_api.push_message(
                                    event.source.user_id, [
                                    TextSendMessage(text=pushmsg),
                                    ]
                                    )
                                    

                    elif command == '/ujian':
                        scrape.ujian(getattr(login,name))
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text=scrape.jadwal)
                            )


    if '/perintah' in text.split():
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="1./absen user\n2./jatah user\n3./elearning user\n4./ujian user\nUntuk mengecek user yang tersedia silahkan ketik /user"))

    elif '/user' in text.split():
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=str(names)))

    elif 'hai' in text.split() or 'halo' in text.split() or 'salken' in text.split() and 'budi' in text.split():
        profile = line_bot_api.get_profile(event.source.user_id)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='Hai, ' + profile.display_name + '\nSaya Budi, budak digital yang siap membantu keperluan bolosmu :D\nSilahkan ketik /perintah jika kamu bingung'))




if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)