from urllib.error import HTTPError, URLError
from urllib.request import urlopen, Request
import requests


TIMEOUT_TIME = 7
LATE_TIME = 5


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
ConnectionError - 808
'''
def check(url_to_check):
    url = url_to_check
    if 'https://' not in url and 'http://' not in url:
        url = 'https://' + url
    response_time = 0
    try:
        response_time = opening_time(url)
        headers = requests.utils.default_headers()
        headers.update({'User-Agent': 'My User Agent 1.0',})
        website = urlopen(Request(url, headers=headers), timeout=TIMEOUT_TIME)
    except HTTPError as error:
        status = error.code
    except URLError as error:
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
    except requests.exceptions.ConnectionError:
        status = 808
    else:
        if response_time >= LATE_TIME:
            status = 199
        else:
            status = website.getcode()
    return status, round(response_time, 3)
