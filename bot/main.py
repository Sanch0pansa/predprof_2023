import telebot
import requests
from threading import Thread
# import datetime

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

Mailing_Mail = smtplib.SMTP_SSL('smtp.yandex.ru:465')
Mailing_Mail.login(bot_mail, mail_password)

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
        except Exception as ex:
            print(ex)
            logging.error("No request to 'bot/check_user/'")
            bot.send_message(message.from_user.id, 'Простите, но сейчас сервер недоступен. Попробуйте позже')
            return

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
    except Exception as ex:
        print(ex)
        logging.error("No request to 'bot/verify_user/'")
        bot.send_message(message.from_user.id,
                         'Простите, но сейчас сервер недоступен. Попробуйте позже через /start')
        return

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
    except Exception as ex:
        print(ex)
        logging.error("No request to 'bot/get_bot_messages/'")
        return

    tg_message = {}
    mail_messages = {}

    def add_message(array, user, text):
        if user in array:
            array[user] += text
        else:
            array[user] = text

    for i in dict_data:
        if i['checked_at'].minute < 10:
            time = f"{i['checked_at'].hour}:0{i['checked_at'].minute}"
        else:
            time = f"{i['checked_at'].hour}:{i['checked_at'].minute}"
        if i['response_status_code'] == '200':
            for tg_id in i['subscribers_telegram']:
                add_message(tg_message, tg_id, '')
            for mail in i['subscribers_email']:
                add_message(mail_messages, mail, '')
        else:
            for tg_id in i['subscribers_telegram']:
                add_message(tg_message, tg_id,
                            f'❌ {i["url"]} Код ошибки: {i["response_status_code"]}, Время проверки: {time}\n')
            for mail in i['subscribers_email']:
                add_message(mail_messages, mail,
                            f'❌ {i["url"]} Код ошибки: {i["response_status_code"]}, Время проверки: {time}\n')

    month = dict_data[0]['checked_at'].month
    day = dict_data[0]['checked_at'].day

    MONTHS = ['Января', 'Февраля', 'Марта', 'Апреля', 'Мая', 'Июня', 'Июля', 'Августа', 'Сентября', 'Октября', 'Ноября',
              'Декабря']
    month = MONTHS[month - 1]

    for tg in tg_message:
        if not tg_message[tg]:
            tg_message[tg] = '✅ Все сайты работают\n'

    for mail in mail_messages:
        if not mail_messages[mail]:
            mail_messages[mail] = '✅ Все сайты работают\n'

    last_data_telegram = tg_message.copy()
    last_data_telegram['date'] = f'Последнее обновление {day} {month}\n'

    for message in tg_message:
        if message == 'date':
            continue
        try:
            bot.send_message(message, last_data_telegram['date'] + tg_message[message], disable_web_page_preview=True)
        except telebot.apihelper.ApiException:
            logging.error(f"Can't send message to {message}")
            continue
        except Exception as ex:
            logging.error(ex)
            print(ex)
            continue

    def send_email(to_mail, text):
        theme = 'Оповещение о работе сайта'
        e_mail = f'From: {bot_mail}\r\nTo: {to_mail}]\r\n' \
                 f'Content-Type: text/plain; charset="utf-8"\r\nSubject: {theme}\r\n\r\n'
        e_mail += text
        Mailing_Mail.sendmail(bot_mail, to_mail, e_mail.encode('utf8'))

    for message in mail_messages:
        send_email(message, f'На момент {day} {month}:\n' +
                   mail_messages[message] + '\nС уважением Site Checker!')


task_client = Thread(target=bot.infinity_polling)
task_flask = Thread(target=lambda: app.run(port=1000))
task_client.start()
task_flask.start()

# Добавить ссылку на сайт
