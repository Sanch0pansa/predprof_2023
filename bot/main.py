import time

import telebot
import requests
from threading import Thread

import smtplib


cofig = [i.split() for i in open('conf.txt').readlines()]

bot = telebot.TeleBot(cofig[0][1])
url = '/api/v1/bot'

bot_mail = cofig[1][1]
mail_password = cofig[2][1]

mail = smtplib.SMTP_SSL('smtp.yandex.ru:465')
mail.login(bot_mail, mail_password)


def registration(message):
    # new_user = requests.post(f'{url}/verify', data={'_token': 123456, 'telegram_id': message.from_user.id})
    # new_user_answer = new_user.json()
    new_user_answer = {'success': 'false'}

    if new_user_answer['success'] == 'true':
        bot.send_message(message.from_user.id, 'Успешная авторизация')
    elif new_user_answer['success'] == 'false':
        bot.send_message(message.from_user.id, '''Ошибка авторизации
Возможно срок действия кода истек или он введен неверно
Введите код еще раз''')
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


def check_messages():
    while True:
        # data = requests.post(f'{url}/get_messages/', data={'_token': 123456})
        # dict_data = data.json()
        dict_data = {
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

        for i in dict_data:
            pass

        time.sleep(60 * 30)  # 30 minutes


def send_email(to_mail, text):
    theme = 'Оповещение о работе сайта'
    message = f'From: {bot_mail}\r\nTo: {to_mail}]\r\nContent-Type: text/plain; charset="utf-8"\r\nSubject: {theme}\r\n\r\n'
    text += 'Пока пустышка'  # Оформить сообщение о работе сайта
    message += text
    mail.sendmail(bot_mail, to_mail, message.encode('utf8'))


task_client = Thread(target=bot.infinity_polling)
task_checking = Thread(target=check_messages)
task_client.start()
task_checking.start()

# Функционал:
#
# Регистрация:
# и проверить код регистрации (запрос на сервер кода по ??? ) (/bot/verify)
# проверка на срок годности кода
#
# если код верный отправляем тг id на сервер get
#
# Запрос на сервер наличия сообщений юзеру и отправка сообщения
# по времени отправляем сообщения
