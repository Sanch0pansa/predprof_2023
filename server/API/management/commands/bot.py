import telebot
from threading import Thread
from datetime import datetime
import json
import smtplib
from django.core.management.base import BaseCommand
from .functions import *
import schedule
import os
from API.views.bot import check_user, get_messages, verify_user
import time

token = "5958220323:AAHE7tbTmY6_YSL6xpupmP3NOgD1muNsYlE"

logging.basicConfig(level=logging.INFO, filename='logs.log', filemode='w',
                    format="%(asctime)s %(levelname)s %(message)s")

my_id = 1080913894

conf = [
    "bot_token: 5958220323:AAHE7tbTmY6_YSL6xpupmP3NOgD1muNsYlE",
    "bot_mail: tochecksite@yandex.ru",
    "mail_password: _qazwsx123",
]

config = [i.split() for i in conf]

bot = telebot.TeleBot(os.environ.get("BOT_TOKEN", config[0][1]))

bot_mail = os.environ.get("BOT_MAIL", config[1][1])
mail_password = os.environ.get("BOT_MAIL_PASSWORD", config[2][1])

try:
    with open('last_data.json', 'r') as file:
        last_data_telegram = json.load(file)
        print('Successful load file\n', last_data_telegram)
except Exception as er:
    last_data_telegram = {}
    print('Unsuccessful load file\n', er)


@bot.message_handler(commands=['help', 'start'])
def bot_start(message):
    if message.text == '/start':
        check = check_user(message.from_user.id)
        if not check:
            bot.send_message(message.from_user.id, 'Простите, но сейчас сервер недоступен. Попробуйте позже')
            return
        elif not check['user_verified']:
            bot.send_message(message.from_user.id, 'Привет!\nОтправьте мне код, который показан на сайте')
            bot.register_next_step_handler(message, registration)
        else:
            bot.send_message(message.from_user.id, 'Ваш телеграмм уже зарегестрирован')
    elif message.text == '/help':
        commands = 'Вот список доступных команд: \n' \
                   '/last - Показать последние статусы сайтов'
        bot.send_message(message.from_user.id, commands)


def registration(message):
    new_user = verify_user(message.from_user.id, message.text)
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


@bot.message_handler(command=['check'])
def admin_commands(message):
    if message.from_user.id != my_id:
        return
    if message.text == '/check':
        try:
            check_bot_messages()
        except Exception as ex:
            print(ex)


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
        check = check_user(message.from_user.id)
        if check['user_verified']:
            bot.send_message(message.from_user.id, last_data_telegram['date'][0] +
                             f"✅ Все сайты работали на момент времени {last_data_telegram['date'][1]}")
        else:
            bot.send_message(message.from_user.id, 'Ваш телеграмм не привязан или остутствует соединение с сервером')


def check_bot_messages():
    global last_data_telegram
    print("Run 'check_bot_messages' function")
    logging.info("Run 'check_bot_messages' function")

    dict_data = get_messages()
    if not dict_data:
        print('No dict_data')
        dict_data = []

    tg_message = {}
    for_last_tg_message = {}

    mail_messages = {}
    print(dict_data)

    print('Processing data')
    for i in dict_data:
        site_time = datetime.strptime(i['checked_at'], '%Y-%m-%dT%H:%M:%S.%f').strftime('%H:%M')
        reasons = ''
        for reason in i['error']["reasons"]:
            reasons += '\n - ' + reason
        message = f'❌ {i["url"]} Время проверки - {site_time}\n' \
                  f'Ошибка: {i["error"]["error_description"]}\n' \
                  f'Возможные причины: {reasons}\n\n'

        for_last_tg_message[message] = i["subscribers_telegram"]

        for tg in i["subscribers_telegram"]:
            add_message(tg_message, tg, message)

        for mail in i['subscribers_email']:
            add_message(mail_messages, mail, message)

    if dict_data:
        date = datetime.strptime(dict_data[0]['checked_at'], '%Y-%m-%dT%H:%M:%S.%f')
    else:
        date = datetime.now()
    month = MONTHS(date.month)
    day = date.day
    for_last_time = date.strftime('%H:%M')

    last_data_telegram = for_last_tg_message.copy()
    last_data_telegram['date'] = [f'Последнее обновление {day} {month}\n', for_last_time]

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
            print(f"Can't send message to {message}")
        except Exception as ex:
            logging.error(ex)
            print(ex)

    print('Send messages to mail')
    with smtplib.SMTP_SSL('smtp.yandex.ru:465') as Mailing_Mail:
        Mailing_Mail.login(bot_mail, mail_password)
        for message in mail_messages:
            try:
                send_email(message, f'На момент {day} {month}:\n' +
                           mail_messages[message] + '\nС уважением Site Checker!',
                           bot_mail, Mailing_Mail)
            except Exception as ex:
                print(ex)


def scheduler():
    schedule.every().minute.at(":00").do(check_bot_messages)
    schedule.every().minute.at(":20").do(check_bot_messages)
    schedule.every().minute.at(":40").do(check_bot_messages)
    while True:
        schedule.run_pending()
        time.sleep(1)


# Название класса обязательно - "Command"
class Command(BaseCommand):
    # Используется как описание команды обычно
    help = 'Implemented to Django application telegram bot setup command'

    def handle(self, *args, **kwargs):
        task_client = Thread(target=bot.infinity_polling)
        task_calendar = Thread(target=scheduler)
        task_client.start()
        task_calendar.start()
