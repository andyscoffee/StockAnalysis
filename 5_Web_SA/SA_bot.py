# 슬랫 봇을 이용한 메시지 전송

import requests
import json


def post_message(token, channel, text, attachments):
    attachments = json.dumps(attachments)
    response = requests.post("https://slack.com/api/chat.postMessage",
                             headers={"Authorization": "Bearer "+token},
                             data={"channel": channel, "text": text,
                                   "attachments": attachments}
                             )


markdown_text = '''
This message is plain.
*This message is bold.*
`This message is code.`
_This message is italic._
~This message is strike.~
'''

attach_dict = {
    "color": '#ff0000',
    "author_name": 'INVESTMENT',
    "title": '오늘의 증시 KOSPI',
    "title_link": 'http://finance.naver.com/sise/sise_index.nhn?code=KOSPI',
    "text": '2,326.13 △11.89 (+0.51%)',
    "image_url": 'https://ssl.pstatic.net/imgstock/chart3/day/KOSPI.png'
}
attach_list = [attach_dict]
myToken = "xoxb-3924346563861-3951022314320-3n6cD9XUpAoySke0rof9m6qc"
post_message(myToken, '#trading', markdown_text, attach_list)
# 슬랙 정책 업데이트로 slacker 사용 불가 requests 형태로 변경
