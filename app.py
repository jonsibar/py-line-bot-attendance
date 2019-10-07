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
import scrape
import login

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
    names = ['jono', 'devina', 'hudiya', 'pikoy', 'jeki']
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
            TextSendMessage(text="1./absen\n2./jatah\n3./elearning\n4./ujian\n5./user"))

    elif '/user' in text.split():
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=str(names)))

    elif 'hai' in text.split() or 'halo' in text.split() or 'salken' in text.split() and 'budi' in text.split():
        profile = line_bot_api.get_profile(event.source.user_id)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='Hai, ' + profile.display_name + '\nSaya Budi, budak digital yang siap membantu keperluan bolosmu :D\nSilahkan ketik /perintah jika kamu bingung'))


    elif 'budi' in text.split():
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="apa bang"))


    elif 'koy' in text.split() or 'qoy' in text.split():
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="kak pikoyyy"))

    elif 'tasnim' in text.split():
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='itu punya kak pikoyyy'))

    elif 'hudiya' and 'fadhil' in text.split():
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='mending fadhil kemana2 lahh'))
    elif 'hud' in text.split():
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='woy dipanggil hud jangan bengong aja'))
    lols = ['wk','kw']
    for lol in lols:
        if lol in text:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='tawa mulu bukan mikir'))
    if 'jangan' in text.split():
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='siapa elu ngatur2?'))
    curses = ['babi', 'babi', 'bangsat', 'bgsd', 'bangsad', 'bgst', 'gblok', 'gblog', 'gblg', 'goblok', 'goblog', 'tolol', 'tlol', 'blog', 'tai']
    for curse in curses:
        if curse in text.split():
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='lo yg '+curse))
    if 'anjing' in text.split() or 'anjg' in text.split():
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=text.replace('anjing', 'pikoy')))
    elif 'daftar' in text.split() or 'cara' in text.split() and 'budi' in text.split():
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='Jika ingin menikmati fiturnya,\nSilahkan chat budi dengan username dan password sso mu'))



if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)