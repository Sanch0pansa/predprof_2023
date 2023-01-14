from site_checker import check

import schedule
import time


def get_urls():
    # тут будут вымогаться jsonы
    urls = ['https://ru.wikipedia.org/wiki/%D0%A1%D0%B0%D0%B9%D1%82']
    return urls


def do():
    return check(get_urls())


schedule.every().hour.do(do)
