import schedule
import time
import requests
from threading import Thread

from site_checker import check


config = {}
for l in open('conf.txt', 'r').readlines():
    config[l.split(': ')[0]] = l.split(': ')[1]
checker_token = config['checker_token'].rstrip('\n')
main_url = 'http://127.0.0.1:8000/api/v1/checker'


class SitechekerThread(Thread):
    def __init__(self, urls):
        Thread.__init__(self)
        self.urls = urls
        self.results = {}

    def run(self):
        time.sleep(1)
        for page_id, url in self.urls:
            self.results[page_id] = check(url)


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
    return urls_data


def check_all_urls():
    urls = get_urls().items()
    threads = []
    for i in range(4):
        t = SitechekerThread(list(urls)[len(urls) * i // 4:len(urls) * (i + 1) // 4])
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    results = {**threads[0].results, **threads[1].results, **threads[2].results, **threads[3].results}

    # Отправка
    response = requests.post(f'{main_url}/check/', json={'_token': checker_token, 'data': results})

    # Логи
    res_for_logs = {}
    for page_id, url in urls:
        res_for_logs[url] = results[page_id]
    with open('logs.log', 'a') as logs:
        for url, info in res_for_logs.items():
            logs.write('\n' + info[2] + ' >>> \t' + str(info[0]) + '\t| ' + str(info[1]) + '\t| ' + url)


schedule.every().hour.do(check_all_urls)
while True:
    schedule.run_pending()
    time.sleep(1)
