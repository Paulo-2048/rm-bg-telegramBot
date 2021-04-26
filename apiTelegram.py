import requests
import json
from time import sleep
from threading import Thread, Lock
import decouple
import apiCut


token = decouple.config('KEY_TOKEN')


global config
config = {'url': 'https://api.telegram.org/bot' +
          token + '/', 'lock': Lock(), 'url_file': 'https://api.telegram.org/file/bot'+token+'/'}


def del_update(data):
    global config

    config['lock'].acquire()
    requests.post(config['url'] + 'getUpdates',
                  {'offset': data['update_id']+1})
    config['lock'].release()


def send_message(data, msg):
    global config

    config['lock'].acquire()
    requests.post(config['url'] + 'sendMessage',
                  {'chat_id': data['message']['chat']['id'], 'text': str(msg)})
    config['lock'].release()


def get_file(file_path):
    global config
    return requests.get(config['url_file'] + str(file_path)).content

def cut_img(arquive_link):
    image_cuted = apiCut.apiCutFunction(arquive_link)

    config['lock'].acquire()
    requests.post(config['url'] + 'sendPhoto',
                  {'chat_id': data['message']['chat']['id'], 'photo': image_cuted})
    config['lock'].release()


while True:

    x = ''
    while True:
        try:
            x = json.loads(requests.get(config['url'] + 'getUpdates').text)
            break

        except Exception as e:
            x = ' '
            if 'Failed to establish a new connection' in str(e):
                print('Perca de conexão')
            else:
                print('Error desconhecido')

    if len(x['result']) > 0:
        for data in x['result']:
            Thread(target=del_update, args=(data,)).start()

            if not 'message' in data:
                break

            elif 'photo' in data['message']:
                photo_archive = json.loads(requests.post(
                    config['url'] + 'getFile?file_id=' + data['message']['photo'][1]['file_id']).text)['result']['file_path']
                file = get_file(photo_archive)
                link = config['url_file'] + photo_archive
                cut_img(link)

            elif 'document' in data['message']:
                file_archive = json.loads(requests.post(
                    config['url'] + 'getFile?file_id=' + data['message']['document']['file_id']).text)['result']['file_path']
                file = get_file(file_archive)
                link = config['url_file'] + file_archive
                cut_img(link)

            elif 'entities' in data['message']:
                if data['message']['text'] == "/start":
                    Thread(target=send_message, args=(
                        data, 'Bot em test, but working...')).start()
                else:
                    Thread(target=send_message, args=(
                        data, 'Unknow Command')).start()
            else:
                Thread(target=send_message, args=(
                    data, 'Send img file or photo archive')).start()

        sleep(2)