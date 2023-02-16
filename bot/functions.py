import requests
import logging

logging.basicConfig(level=logging.INFO, filename='logs.log', filemode='w',
                    format="%(asctime)s %(levelname)s %(message)s")


def add_message(array, user, text):
    if user in array:
        array[user] += text
    else:
        array[user] = text


def send_email(to_mail, text, bot_mail, mail):
    theme = 'Оповещение о работе сайта'
    e_mail = f'From: {bot_mail}\r\nTo: {to_mail}]\r\n' \
             f'Content-Type: text/plain; charset="utf-8"\r\nSubject: {theme}\r\n\r\n'
    e_mail += text
    mail.sendmail(bot_mail, to_mail, e_mail.encode('utf8'))


def try_connect(url, data):
    try:
        get_data = requests.post(url, data=data)
        get_data = get_data.json()
        return get_data
    except Exception as ex:
        print(ex, f'no connect to {url}')
        logging.error(f"No request to {url}")
        return False


def MONTHS(number):
    months = ['Января', 'Февраля', 'Марта', 'Апреля', 'Мая', 'Июня', 'Июля', 'Августа', 'Сентября', 'Октября', 'Ноября',
              'Декабря']
    return months[number - 1]
