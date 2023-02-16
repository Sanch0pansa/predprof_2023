import telebot
from threading import Thread
from datetime import datetime
import json
import smtplib
from flask import Flask, request

from functions import *

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

try:
    with open('last_data.json', 'r') as file:
        last_data_telegram = json.load(file)
        print('Successful load file\n', last_data_telegram)
except Exception as er:
    last_data_telegram = {}
    print('Unsuccessful load file\n', er)

Mailing_Mail = smtplib.SMTP_SSL('smtp.yandex.ru:465')
Mailing_Mail.login(bot_mail, mail_password)


@app.post('/check_messages')
def url_get_messages():
    data = request.get_json()
    if data['_token'] == _token:
        print('Call from server')
        logging.info('Call from server')
        try:
            check_bot_messages()
        except Exception as ex:
            print(ex)
    else:
        logging.info('Call from OUTSIDE')
    print('End Check')
    return 'None'


@bot.message_handler(commands=['help', 'start'])
def bot_start(message):
    if message.text == '/start':
        check = try_connect(f'{url}/check_user/', {'_token': _token, 'telegram_id': message.from_user.id})
        if not check:
            bot.send_message(message.from_user.id, 'Простите, но сейчас сервер недоступен. Попробуйте позже')
            return
        elif not check['user_verified']:
            bot.send_message(message.from_user.id,
                             '''Привет!\nОтправьте мне код, который показан на сайте''')
            bot.register_next_step_handler(message, registration)
        else:
            bot.send_message(message.from_user.id, 'Ваш телеграмм уже зарегестрирован')
    elif message.text == '/help':
        commands = '''Вот список доступных команд:
/last - Показать последние статусы сайтов
'''
        bot.send_message(message.from_user.id, commands)


def registration(message):
    new_user = try_connect(f'{url}/verify_user/', {'_token': _token, 'telegram_id': message.from_user.id,
                                                   'telegram_verification_code': message.text})
    if not new_user:
        bot.send_message(message.from_user.id,
                         'Простите, но сейчас сервер недоступен. Попробуйте позже через /start')
        return
    elif new_user['success']:
        bot.send_message(message.from_user.id, 'Готово. Теперь можете пользоваться ботом')
    elif not new_user['success']:
        bot.send_message(message.from_user.id, 'Ошибка авторизации\n'
                                               'Возможно срок действия кода истек или он введен неверно\n'
                                               'Проверьте и введите код еще раз')
        bot.register_next_step_handler(message, registration)

    logging.info(f'Message {message.text} from {message.from_user.id}')


@bot.message_handler(commands=['last'])
def bot_reply(message):
    print(last_data_telegram)
    logging.info(f"Message '{message.text}' from {message.from_user.id}")
    if not last_data_telegram:
        bot.send_message(message.from_user.id, 'Данных пока нет')
        logging.error('No last data')
        return
    reply = ''
    for key in last_data_telegram:
        if message.from_user.id in last_data_telegram[key]:
            reply += key

    if reply:
        bot.send_message(message.from_user.id, last_data_telegram['date'][0] +
                         reply, disable_web_page_preview=True)
    else:
        bot.send_message(message.from_user.id, last_data_telegram['date'][0] +
                         f"✅ Все сайты работали на момент времени {last_data_telegram['date'][1]}")


def check_bot_messages():
    global last_data_telegram
    print("Run 'check_bot_messages' function")
    logging.info("Run 'check_bot_messages' function")

    dict_data = try_connect(f'{url}/get_bot_messages/', {'_token': _token})
    if not dict_data:
        print('No dict_data')
        dict_data = []

    tg_message = {}
    for_last_tg_message = {}

    mail_messages = {}
    print(dict_data)

    print('Processing data')
    for i in dict_data:
        time = datetime.strptime(i['checked_at'], '%Y-%m-%dT%H:%M:%S.%f').strftime('%H:%M')
        reasons = ''
        for reason in i['error']["reasons"]:
            reasons += '\n - ' + reason
        message = f'❌ {i["url"]} Время проверки - {time}\n'\
                  f'Ошибка: {i["error"]["error_description"]}\n' \
                  f'Возможные причины: {reasons}\n'

        for_last_tg_message[message] = i["subscribers_telegram"]

        for tg in i["subscribers_telegram"]:
            add_message(tg_message, tg, message)

        for mail in i['subscribers_email']:
            add_message(mail_messages, mail, message)

    if dict_data:
        date = datetime.strptime(dict_data[0]['checked_at'], '%Y-%m-%dT%H:%M:%S.%f')
    else:
        date = datetime.now()
        print(date)
    month = MONTHS(date.month)
    day = date.day
    time = date.strftime('%H:%M')

    last_data_telegram = for_last_tg_message.copy()
    last_data_telegram['date'] = [f'Последнее обновление {day} {month}\n', time]

    print('Load the last date to file')
    with open('last_data.json', 'w') as write_file:
        json.dump(last_data_telegram, write_file)

    print('Send messages to telegram')
    for message in tg_message:
        if message == 'date':
            continue
        try:
            bot.send_message(message, last_data_telegram['date'][0] + tg_message[message],
                             disable_web_page_preview=True)
        except telebot.apihelper.ApiException:
            logging.error(f"Can't send message to {message}")
        except Exception as ex:
            logging.error(ex)
            print(ex)

    print('Send messages to mail')
    for message in mail_messages:
        try:
            send_email(message, f'На момент {day} {month}:\n' +
                       mail_messages[message] + '\nС уважением Site Checker!',
                       bot_mail, Mailing_Mail)
        except Exception as ex:
            print(ex)


task_client = Thread(target=bot.infinity_polling)
task_flask = Thread(target=lambda: app.run(port=1000))
task_client.start()
task_flask.start()

# Добавить ссылку на сайт
