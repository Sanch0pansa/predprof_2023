from urllib.error import HTTPError, URLError
from urllib.request import urlopen, Request
from urllib.parse import urlparse
import requests
from datetime import datetime
import pytz
import ping3


TIMEOUT_TIME = 7


def opening_time(url):
    return requests.get(url).elapsed.total_seconds()


'''
Особые статусы:

ConnectionError - 503
Unknown Error - 520
Timeout - 522, 524
'''
def check(url_to_check, check_num=0):
    url = url_to_check
    if 'https://' not in url and 'http://' not in url:
        url = 'https://' + url
    response_time = 0
    try:
        headers = requests.utils.default_headers()
        headers.update({'User-Agent': 'My User Agent 1.0',})
        website = urlopen(Request(url, headers=headers), timeout=TIMEOUT_TIME)
        response_time = opening_time(url)
    except HTTPError as error:
        status = error.code
    except URLError as error:
        if error.reason.args[0] == '_ssl.c:1106: The handshake operation timed out':
            status = 524
        else:
            status = 520
            if check_num < 4:
                return check(url_to_check, check_num + 1)
    except requests.exceptions.ConnectionError:
        status = 503
        if check_num < 4:
            return check(url_to_check, check_num + 1)
    except socket.timeout:
        domain = urlparse(url).netloc
        if not bool(ping3.ping(domain)):
            status = 522
        else:
            status = 524
    else:
        status = website.getcode()
    return status, int(response_time * 1000), datetime.now(pytz.timezone('Europe/Moscow')).isoformat()
