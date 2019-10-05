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
			TextSendMessage(text='Pake aku kak ' + profile.display_name)
			)

@handler.add(JoinEvent)
def handle_join(event):
	line_bot_api.reply_message(
			event.reply_token,
			TextSendMessage(text='Pake aku kak')
			)



@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
	text = event.message.text.lower()
	#profile = line_bot_api.get_profile(event.source.user_id)

	if text == 'absen jono':
		scrape.presensi(login.jono)
		line_bot_api.reply_message(
			event.reply_token,
			TextSendMessage(text=scrape.attendance)
			)
	elif text == 'elearning jono':
		scrape.mats(login.jono)
		for pushmsg in scrape.elearning_list:
			line_bot_api.push_message(
				event.source.user_id, [
				TextSendMessage(text=pushmsg),
				]
			)




	elif text == 'absen devina':
		presensi(login.devina)
		line_bot_api.reply_message(
			event.reply_token,
			TextSendMessage(text=scrape.attendance)
			)
	elif text == 'elearning devina':
		scrape.mats(login.devina)
		for pushmsg in scrape.elearning_list:
			line_bot_api.push_message(
				event.source.user_id, [
				TextSendMessage(text=pushmsg),
				]
			)





	elif text == 'absen hudiya':
		scrape.presensi(login.hudiya)
		line_bot_api.reply_message(
			event.reply_token,
			TextSendMessage(text=scrape.attendance)
			)
	elif text == 'elearning hudiya':
		scrape.mats(login.hudiya)
		for pushmsg in scrape.elearning_list:
			line_bot_api.push_message(
				event.source.user_id, [
				TextSendMessage(text=pushmsg),
				]
			)


	elif text == 'absen pikoy':
		presensi(login.pikoy)
		line_bot_api.reply_message(
			event.reply_token,
			TextSendMessage(text=scrape.attendance)
			)
	elif text == 'elearning pikoy':
		scrape.mats(login.pikoy)
		for pushmsg in scrape.elearning_list:
			line_bot_api.push_message(
				event.source.user_id, [
				TextSendMessage(text=pushmsg),
				]
			)





if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)