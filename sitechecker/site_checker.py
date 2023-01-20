import urllib.request
import requests
from time import time
from datetime import datetime


TIMEOUT_TIME = 7
FIGOVO_GRUZIT_TIME = 5


def opening_time(url):
    return requests.get(url).elapsed.total_seconds()


'''
Всё хорошо - 200
Плохо грузит - 199
Timeout - 0
Hostname mismatch - 1
getaddrinfo failed - 2
Непонятная фигня с URLError - 666

Not Found - 404
Method Not Allowed - 405
Not Acceptable - 406
и т.д. для HTTPError

unknown url type - -1
'''
def check(url):
    try:
        website = urllib.request.urlopen(url, timeout=TIMEOUT_TIME)
    except urllib.error.HTTPError as error:
        status = error.code
    except urllib.error.URLError as error:
        if error.reason.args[0] == '_ssl.c:1106: The handshake operation timed out':
            status = 0
        elif error.reason.args[0] == 1:
            status = 1
        elif error.reason.args[0] == 11001:
            status = 2
        else:
            status = 666
    except ValueError:
        status = -1
    else:
        if opening_time(url) < FIGOVO_GRUZIT_TIME:
            status = website.getcode()
        else:
            status = 199
    return status, datetime.now()
