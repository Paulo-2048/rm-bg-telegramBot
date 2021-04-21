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
    print(arquive_link)
    image_cuted = apiCut.apiCutFunction(arquive_link)
    print(image_cuted)

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
            print(json.dumps(data, indent=1))

            if not 'message' in data:
                break

            elif 'photo' in data:
                pass

            elif 'document' in data['message']:
                file_archive = json.loads(requests.post(
                    config['url'] + 'getFile?file_id=' + data['message']['document']['file_id']).text)['result']['file_path']
                file = get_file(file_archive)
                link = config['url_file'] + file_archive
                cut_img(link)

            elif 'entities' in data['message']:
                if data['message']['text'] == "/start":
                    Thread(target=send_message, args=(
                        data, 'Bot em contrução, lançamento em breve, aguarde...')).start()
                else:
                    Thread(target=send_message, args=(
                        data, 'Commando desconhecido')).start()
            else:
                Thread(target=send_message, args=(
                    data, 'Use / for commands')).start()
            Thread(target=send_message, args=(
                data, 'Em Manutenção')).start()

        sleep(2)