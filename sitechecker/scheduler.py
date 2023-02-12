import schedule
import time
import requests

from site_checker import check


config = {}
for l in open('conf.txt', 'r').readlines():
    config[l.split(': ')[0]] = l.split(': ')[1]
checker_token = config['checker_token'].rstrip('\n')
main_url = 'http://127.0.0.1:8000/api/v1/checker'


def get_urls():
    data = requests.post(f'{main_url}/get_pages_for_check/', data={'_token': checker_token})
    urls_data = data.json()
    '''urls_data = {
        "1": "https://donstu.ru",
        "4": "https://www.msu.ru",
        "5": "https://www.mirea.ru",
        "6": "https://mephi.ru",
        "8": "https://mtuci.ru",
        "9": "https://www.ranepa.ru",
        "29": "https://mai.ru",
        "17": "https://www.sevsu.ru",
        "30": "https://itmo.ru",
        "31": "http://www.simbip.ru",
        "3": "https://misis.ru",
        "33": "https://www.tsu.ru"
    }'''
    return urls_data.items()


def check_all_urls():
    results = {}
    res_for_logs = {}
    for page_id, url in get_urls():
        res = check(url)
        results[page_id] = res
        res_for_logs[url] = res
    print(results)

    # Отправка
    response = requests.post(f'{main_url}/check/', json={'_token': checker_token, 'data': results})
    print(response.json())

    # Логи
    with open('logs.log', 'a') as logs:
        for url, info in res_for_logs.items():
            logs.write('\n' + info[2] + ' >>> \t' + str(info[0]) + '\t| ' + str(info[1]) + '\t| ' + url)


schedule.every().hour.do(check_all_urls)
while True:
    schedule.run_pending()
    time.sleep(1)
