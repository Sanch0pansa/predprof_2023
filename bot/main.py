import telebot
import requests
from threading import Thread
import datetime

import logging

import smtplib

from flask import Flask, request

app = Flask('SiteChecker')

logging.basicConfig(level=logging.INFO, filename='logs.log', filemode='w',
                    format="%(asctime)s %(levelname)s %(message)s")

my_id = 1080913894


with open('conf.txt') as file:
    config = [i.split() for i in file.readlines()]

    _token = config[3][1]
    bot = telebot.TeleBot(config[0][1])
    url = config[4][1]

    bot_mail = config[1][1]
    mail_password = config[2][1]

mail = smtplib.SMTP_SSL('smtp.yandex.ru:465')
mail.login(bot_mail, mail_password)

last_data_telegram = {}


@app.post('/check_messages')
def url_get_messages():
    data = request.get_json()
    if data['_token'] == _token:
        logging.info('Call from server')
        check_bot_messages()
    else:
        logging.info('Call from OUTSIDE')
    return 'None'


@bot.message_handler(commands=['help', 'start'])
def bot_start(message):
    if message.text == '/start':  # проверяем на наличие юзера
        try:
            check = requests.post(f'{url}/check_user/', data={'_token': _token, 'telegram_id': message.from_user.id})
            check = check.json()
        except:
            logging.error("No request to 'bot/check_user/'")
            bot.send_message(message.from_user.id, 'Простите, но сейчас сервер недоступен. Попробуйте позже')
            return
        # check = {
        #     'user_verified': False
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


def registration(message):
    try:
        new_user = requests.post(f'{url}/verify_user/', data={'_token': _token, 'telegram_id': message.from_user.id,
                                                              'telegram_verification_code': message.text})
        new_user_answer = new_user.json()
    except:
        logging.error("No request to 'bot/verify_user/'")
        bot.send_message(message.from_user.id,
                         'Простите, но сейчас сервер недоступен. Попробуйте позже через /start')
        return
    # if message.text == '86573':
    #     new_user_answer = {'success': True}
    # else:
    #     new_user_answer = {'success': False}

    if new_user_answer['success']:
        bot.send_message(message.from_user.id, 'Готово. Теперь можете пользоваться ботом')
    elif not new_user_answer['success']:
        bot.send_message(message.from_user.id, '''Ошибка авторизации
Возможно срок действия кода истек или он введен неверно
Проверьте и введите код еще раз''')
        bot.register_next_step_handler(message, registration)

    logging.info(f'Message {message.text} from {message.from_user.id}')


@bot.message_handler(commands=['last'])
def bot_reply(message):
    logging.info(f"Message '{message.text}' from {message.from_user.id}")
    if not last_data_telegram:
        bot.send_message(message.from_user.id, 'Данных пока нет')
        logging.error('No last data')
        return
    try:
        bot.send_message(message.from_user.id, last_data_telegram['date'] + last_data_telegram[message.from_user.id],
                         disable_web_page_preview=True)
    except KeyError:
        bot.send_message(message.from_user.id,
                         'Вы не подписанны не на один сайт. \n Вы можете сделать это через официальный сайт ...')
        logging.info("'/last' from not subscriber")


# @bot.message_handler(commands=['check'])
def check_bot_messages():
    global last_data_telegram
    logging.info("Run 'check_bot_messages' function")
    try:
        data = requests.post(f'{url}/get_bot_messages/', data={'_token': _token})
        dict_data = data.json()
    except:
        logging.error("No request to 'bot/get_bot_messages/'")
        return
    # dict_data = [
    #     {
    #         'url': 'https://dontsu.ru',  # 2xx - хороший сайт
    #         'response_status_code': '900',  # 4xx - ошибка клиента
    #         'response_time': 32767,  # 5xx - ошибка сервера
    #         'subscribers_telegram': [
    #             1080913894,
    #             # 5694956479
    #         ],
    #         'subscribers_email': [
    #             # 'andrew.lipko@yandex.ru',
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
    #             # 'andrew.lipko@yandex.ru',
    #             # 'lde0060@gmail.com',
    #         ]
    #     },
    # ]
    tg_message = {}
    mail_messages = {}

    def add_message(array, user, text):
        if user in array:
            array[user] += text
        else:
            array[user] = text

    for i in dict_data:
        if i['response_status_code'] == '200':
            for id in i['subscribers_telegram']:
                add_message(tg_message, id, '')
            for mail in i['subscribers_email']:
                add_message(mail_messages, mail, '')
        elif i['response_status_code'][0] == '4':
            for id in i['subscribers_telegram']:
                add_message(tg_message, id, f'❌ {i["url"]} (ошибка клиента)\n')
            for mail in i['subscribers_email']:
                add_message(mail_messages, mail, f'❌ {i["url"]} (ошибка клиента)\n')
        elif i['response_status_code'][0] == '5':
            for id in i['subscribers_telegram']:
                add_message(tg_message, id, f'❌ {i["url"]} (ошибка сервера) \n')
            for mail in i['subscribers_email']:
                add_message(mail_messages, mail, f'❌ {i["url"]} (ошибка сервера) \n')
        else:
            for id in i['subscribers_telegram']:
                add_message(tg_message, id, f'❌ {i["url"]} \n')
            for mail in i['subscribers_email']:
                add_message(mail_messages, mail, f'❌ {i["url"]} \n')

    MONTHS = ['Января', 'Февраля', 'Марта', 'Апреля', 'Мая', 'Июня', 'Июля', 'Августа', 'Сентября', 'Октября', 'Ноября',
              'Декабря']
    month = MONTHS[datetime.date.today().month - 1]
    day = datetime.date.today().day
    current_time = datetime.datetime.now().time().isoformat()[:5]

    for id in tg_message:
        if not tg_message[id]:
            tg_message[id] = '✅ Все сайты работают'

    for mail in mail_messages:
        if not mail_messages[mail]:
            mail_messages = '✅ Все сайты работают'

    last_data_telegram = tg_message.copy()
    last_data_telegram['date'] = f'Последнее обновление {day} {month} в {current_time}\n'

    for message in tg_message:
        if message == 'date':
            continue
        try:
            bot.send_message(message, last_data_telegram['date'] + tg_message[message], disable_web_page_preview=True)
        except telebot.apihelper.ApiException:
            logging.error(f"Can't send message to {message}")
            continue
        except Exception as ex:
            logging.error(f"ex")
            print(ex)
            continue

    def send_email(to_mail, text):
        theme = 'Оповещение о работе сайта'
        message = f'From: {bot_mail}\r\nTo: {to_mail}]\r\nContent-Type: text/plain; charset="utf-8"\r\nSubject: {theme}\r\n\r\n'
        message += text
        mail.sendmail(bot_mail, to_mail, message.encode('utf8'))

    for message in mail_messages:
        send_email(message, f'На момент {day} {month} {current_time}:\n' +
                   mail_messages[message] + '\nС уважением Bot Checker!')


task_client = Thread(target=bot.infinity_polling)
task_flask = Thread(target=lambda: app.run(port=1000))
task_client.start()
task_flask.start()

# Сделать получение времени
# Добавить ссылку на сайт
