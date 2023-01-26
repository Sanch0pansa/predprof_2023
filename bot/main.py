import time


import telebot
import requests
from threading import Thread
from timeloop import Timeloop
import datetime

import smtplib

tl = Timeloop()

my_id = 1080913894

config = [i.split() for i in open('conf.txt').readlines()]

_token = config[3][1]
bot = telebot.TeleBot(config[0][1])
url = 'http://127.0.0.1:8000/api/v1/bot'

bot_mail = config[1][1]
mail_password = config[2][1]

mail = smtplib.SMTP_SSL('smtp.yandex.ru:465')
mail.login(bot_mail, mail_password)

last_data_telegram = {}



def registration(message):
    new_user = requests.post(f'{url}/verify_user/', data={'_token': _token, 'telegram_id': message.from_user.id,
                                                          'telegram_verification_code': message.text})
    new_user_answer = new_user.json()
    # new_user_answer = {'success': True}

    if new_user_answer['success']:
        bot.send_message(message.from_user.id, 'Готово. Теперь можете пользоваться ботом')
    elif not new_user_answer['success']:
        bot.send_message(message.from_user.id, '''Ошибка авторизации
Возможно срок действия кода истек или он введен неверно
Проверьте и введите код еще раз''')
        bot.register_next_step_handler(message, registration)


@bot.message_handler(commands=['help', 'start'])
def bot_start(message):
    if message.text == '/start':  # проверяем на наличие юзера
        # print(message)

        check = requests.post(f'{url}/check_user/', data={'_token': _token, 'telegram_id': message.from_user.id})
        check = check.json()
        # check = {
        #     'user_verified': 'true'
        # }
        if not check['user_verified']:

            bot.send_message(message.from_user.id,
                             '''Привет!\nОтправьте мне код аунтификации, который высвечен на сайте''')

            bot.register_next_step_handler(message, registration)
        else:
            bot.send_message(message.from_user.id, 'Ваш телеграмм уже зарегестрирован')
    elif message.text == '/help':
        commands = '''Вот список доступных команд:

/last - Показать последние статусы сайтов
'''
        bot.send_message(message.from_user.id, commands)


@bot.message_handler(commands=['last'])
def bot_reply(message):
    if message.text == '/last':

        try:
            bot.send_message(message.from_user.id,
                             last_data_telegram['date'] + last_data_telegram[message.from_user.id],
                             disable_web_page_preview=True)
        except KeyError:
            bot.send_message(message.from_user.id, 'Данных пока нет')


# @bot.message_handler(commands=['check'])
@tl.job(interval=datetime.timedelta(minutes=30))  # 30 minutes
def check_bot_messages(message):
    global last_data_telegram
    data = requests.post(f'{url}/get_bot_messages/', data={'_token': _token})
    dict_data = data.json()
    # dict_data = [
    #     {
    #         'url': 'https://dontsu.ru',  # 2xx - хороший сайт
    #         'response_status_code': '900',  # 4xx - ошибка клиента
    #         'response_time': 32767,  # 5xx - ошибка сервера

    #         'subscribers_telegram': [
    #             1080913894,
    #         ],
    #         'subscribers_email': [
    #             'andrew.lipko@yandex.ru',
    #         ]
    #     },
    #     {
    #         'url': 'https://mgu.ru',
    #         'response_status_code': '506',
    #         'response_time': 124,
    #         'subscribers_telegram': [
    #             1080913894,


    #         ],
    #         'subscribers_email': [
    #             'andrew.lipko@yandex.ru',
    #             'lde0060@gmail.com',
    #         ]
    #     },
    # ]
    tg_message = {}
    mail_error_messages = {}


    def add_message(array, user, text):
        if user in array:
            array[user] += text
        else:
            array[user] = text

    for i in dict_data:
        if i['response_status_code'] == '200':
            for id in i['subscribers_telegram']:
                add_message(tg_message, id, f'✅ {i["url"]} \n')
            for mail in i['subscribers_email']:
                add_message(mail_error_messages, mail, f'✅ {i["url"]}\n')

        elif i['response_status_code'][0] == '4':
            for id in i['subscribers_telegram']:
                add_message(tg_message, id, f'❌ {i["url"]} (ошибка клиента)\n')
            for mail in i['subscribers_email']:
                add_message(mail_error_messages, mail, f'❌ {i["url"]} (ошибка клиента)\n')
        elif i['response_status_code'][0] == '5':
            for id in i['subscribers_telegram']:
                add_message(tg_message, id, f'❌ {i["url"]} (ошибка сервера) \n')
            for mail in i['subscribers_email']:
                add_message(mail_error_messages, mail, f'❌ {i["url"]} (ошибка сервера) \n')
        else:
            for id in i['subscribers_telegram']:
                add_message(tg_message, id, f'❌ {i["url"]} \n')
            for mail in i['subscribers_email']:
                add_message(mail_error_messages, mail, f'❌ {i["url"]} \n')

    MONTHS = ['Января', 'Февраля', 'Марта', 'Апреля', 'Мая', 'Июня', 'Июля', 'Августа', 'Сентября', 'Октября', 'Ноября',
              'Декабря']
    month = MONTHS[datetime.date.today().month - 1]
    day = datetime.date.today().day
    current_time = datetime.datetime.now().time().isoformat()[:5]

    last_data_telegram = tg_message.copy()

    last_data_telegram['date'] = f'Последнее обновление {day} {month} в {current_time}\n'

    for message in tg_message:
        if message == 'date':
            continue
        try:
            bot.send_message(message, last_data_telegram['date'] + tg_message[message], disable_web_page_preview=True)

        except telebot.apihelper.ApiException:
            print(f'Нельзя отправить сообщение {message}')
            continue
        except Exception as ex:
            print(ex)
            continue
    for message in mail_error_messages:

        send_email(message, f'На момент {day} {month} {current_time} не работали сайты:\n' +

                   mail_error_messages[message] + '\nС уважением Bot Checker!')


def send_email(to_mail, text):
    theme = 'Оповещение о работе сайта'
    message = f'From: {bot_mail}\r\nTo: {to_mail}]\r\nContent-Type: text/plain; charset="utf-8"\r\nSubject: {theme}\r\n\r\n'
    message += text
    mail.sendmail(bot_mail, to_mail, message.encode('utf8'))


task_client = Thread(target=bot.infinity_polling)
task_client.start()
tl.start(block=True)

