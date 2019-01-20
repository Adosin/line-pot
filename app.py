from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, StickerSendMessage
)

app = Flask(__name__)

line_bot_api = LineBotApi('PcdpFMidni2BaIcwWeKpGqRQh2emKkCKPGI1o5AIHLkQm5Qk5s/qHyXPrGuhsJX6tiSMPwq6HOHY00OqcvNl/mtzY7AoAruWBM9CxNA5R4jvuDZPA4V7JZm8kemreawPIWesqk0W5Vs8Eu4YmC3yiQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('50183bc5af3889b80ac01c81f70c3b96')


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
    msg = event.message.text  # 使用者傳來
    r = '很抱歉, 你說甚麼!'  # 機器人回傳

    if '貼圖' in msg:
        sticker_message = StickerSendMessage(
            package_id='1',
            sticker_id='1'
        )

        line_bot_api.reply_message(
            event.reply_token,
            sticker_message)  

        return # 結束程式, 以下不執行

    if msg in ['hi', 'hi!', 'Hi', 'Hi!']:
        r == '海!'
    elif msg in ['你吃飯了嗎', '你吃飯了嗎?']:
        r = '還沒'
    elif msg == '你是誰':
        r = '我是機器人'
    elif '訂位' in msg:
        r = '你想訂位, 是嗎?'
    


    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r))
        


if __name__ == "__main__":
    app.run()