import telebot
import requests
from threading import Thread

bot = telebot.TeleBot('5981300300:AAH3cU-Px8CPJVSu0mNSX9HkO3Q_rNWxsdM')
my_id = 1080913894


def get_request_message(message):
    pass


# data = requests.post()
# dict_data = data.json()
data = {
    'message': [
        {
            'email': 'andrew.lipko@yandex.ru',
            'message_text': 'Something that is important'
        }, {
            'email': 'andrewlipko123@gmai.com',
            'message_text': 'Something that is important 2'
        }
    ]
}

@bot.message_handlers(command=['start'])
def bor_start(message):
    print(message)
    bot.send_message(message.id, 'Привет')



# Функционал:
#
# Регистрация: Спросить почту
# и проверить код регистрации (запрос на сервер кода по ??? ) (/bot/verify)
# проверка на срок годности кода
#
# если код верный отправляем тг id на сервер get
#
# Запрос на сервер наличия сообщений юзеру и отправка сообщения
# по времени отправляем сообщения


