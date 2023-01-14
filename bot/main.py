import telebot
import requests
from threading import Thread
import asyncio


file = open('conf.txt').readlines()
bot = telebot.TeleBot(file[0].split()[1])
my_id = 1080913894
url = '/api/v1/bot'


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


def registration(message):
    # new_user = requests.post(f'{url}/verify', data={'_token': 123456, 'telegram_id': message.from_user.id})
    # new_user_answer = new_user.json()
    new_user_answer = {'success': 'true'}

    if new_user_answer['success'] == 'true':
        bot.send_message(message.from_user.id, 'Успешная авторизация')
    elif new_user_answer['success'] == 'false':
        bot.send_message(message.from_user.id, '''Ошибка авторизации
Введите код еще раз''')                     # проверить срок годности ?
        bot.register_next_step_handler(message, registration)


@bot.message_handler(commands=['help', 'start'])
def bot_start(message):
    # print(message)
    if message.text == '/start':  # проверяем на наличие юзера

        # check = requests.post(f'{url}/check_user/', data={'_token': 123456, 'telegram_id': message.from_user.id})
        # check = check.json()
        check = {
            'user_verified': 'false'
        }

        if check['user_verified'] == 'false':
            bot.send_message(message.from_user.id,
                             '''Привет!\nОтправьте мне код аунтификации, который высвечен на сайте''')

            bot.register_next_step_handler(message, registration)
        else:
            bot.send_message(message.from_user.id, 'Ваш телеграмм уже зарегестрирован')
    elif message.text == '/help':
        commands = '''Вот список доступных команд:
...
'''
        bot.send_message(message.from_user.id, commands)


task_client = Thread(target=bot.infinity_polling)
task_client.start()


# Функционал:
#
# Регистрация: Спросить почту ?
# и проверить код регистрации (запрос на сервер кода по ??? ) (/bot/verify)
# проверка на срок годности кода
#
# если код верный отправляем тг id на сервер get
#
# Запрос на сервер наличия сообщений юзеру и отправка сообщения
# по времени отправляем сообщения
