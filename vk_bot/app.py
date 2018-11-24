#! /usr/bin/python3

from flask import Flask, request, json
from settings import token, confirmation_token
import vk
from time import sleep

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello from Flask!'

@app.route('/', methods=['POST'])
def processing():
    #Распаковываем json из пришедшего POST-запроса
    data = json.loads(request.data)
    #Вконтакте в своих запросах всегда отправляет поле типа
    if 'type' not in data.keys():
        return 'not vk'
    if data['type'] == 'confirmation':
        return confirmation_token
    elif data['type'] == 'message_new':
        session = vk.Session()
        api = vk.API(session, v=5.80)
        chat_id = data['object']['peer_id'] - 2000000000
        message_text = data['object']['text']
        api.messages.send(access_token=token, chat_id=str(chat_id), message=message_text)
        # Сообщение о том, что обработка прошла успешно
        return 'ok'

session = vk.Session()
api = vk.API(session, v=5.80)

messages = api.messages.get(access_token=token, count=1)
last = messages['items'][0]['id']

while True:
    try:
        messages = api.messages.get(access_token=token, last_message_id=last)
    except Exception as e:
        print(e)
        sleep(4)
        continue
    if not messages['items']: # Если нет новых сообщений
        sleep(4)
        continue
    last = messages['items'][0]['id']
    for message in messages['items']:
        chat_id = message['peer_id'] - 2000000000
        message_text = message['text']
        api.messages.send(access_token=token, chat_id=str(chat_id), message=message_text)