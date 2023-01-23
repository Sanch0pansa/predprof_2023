from site_checker import check
import schedule
import time
import requests


config = [i.split() for i in open('conf.txt').readlines()]
checker_token = config[0][1]
main_url = 'http://127.0.0.1:8000/api/v1/checker'


def get_urls():
    data = requests.post(f'{main_url}/get_pages_for_check/', data={'_token': checker_token})
    urls_data = data.json()
    urls = urls_data[0]['pages']

    #urls = ['dstu.ru', 'donstu.ru']
    return urls


def check_all_urls():
    results = {}
    for url in get_urls():
        results[url] = check(url)

    print(results)

    # Отправка


    # Логи
    with open('logs.log', 'a') as logs:
        for url, info in results.items():
            logs.write('\n' + str(info[0].strftime("%d-%b-%Y %H:%M:%S")) + ' >>> \t' + str(info[1]) + '\t| ' + str('%.3f' % info[2]) + '\t| ' + str(url))


schedule.every().second.do(check_all_urls)
while True:
    schedule.run_pending()
    time.sleep(1)
