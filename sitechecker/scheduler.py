import schedule
import time
import requests
from datetime import datetime

from site_checker import check


config = {}
for l in open('conf.txt', 'r').readlines():
    config[l.split(': ')[0]] = l.split(': ')[1]
checker_token = config['checker_token'].rstrip('\n')
main_url = 'http://127.0.0.1:8000/api/v1/checker'


def get_urls():
    data = requests.post(f'{main_url}/get_pages_for_check/', data={'_token': checker_token})
    urls_data = data.json()
    urls = urls_data['pages']
    #urls = ['donstu.ru', 'https://donstu.ru']
    return urls


def check_all_urls():
    results = {}
    for url in get_urls():
        results[url] = check(url)

    print(results)

    # Отправка
    for url, info in results.items():
        response = requests.post(f'{main_url}/check/', data={'_token': checker_token, 'url': url, 'response_status_code': info[0], 'response_time': info[1]})
        print(response.json())

    # Логи
    with open('logs.log', 'a') as logs:
        for url, info in results.items():
            logs.write('\n' + str(datetime.now().strftime("%d-%b-%Y %H:%M:%S")) + ' >>> \t' + str(info[0]) + '\t| ' + str('%.3f' % info[1]) + '\t| ' + str(url))


schedule.every().hour.do(check_all_urls)
while True:
    schedule.run_pending()
    time.sleep(1)
