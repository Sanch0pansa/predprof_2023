from site_checker import check
import schedule
import time


def get_urls():
    # тут будут вымогаться jsonы
    urls = ['https://ru.wikipedia.org/wiki/%D0%A1%D0%B0%D0%B9%D1%82',
            'https://ru.wikipedia.org/wiki/dsg0%B0%D0%B9%D1%82',
            'https://ru.wikipedia.org/wiki/dsg0%B0%/D0%B9%/D1%82',
            'https://ru.wiki/pediaorg']
    return urls


def check_all_urls():
    results = {}
    for url in get_urls():
        results[url] = check(url)

    # Логи
    with open('logs.log', 'a') as logs:
        for url, status in results.items():
            logs.write('\n' + str(status[1].strftime("%d-%b-%Y %H:%M:%S")) + ' >>> \t' + str(status[0]) + '\t| ' + str(url))


schedule.every().hour.do(check_all_urls)
while True:
    schedule.run_pending()
    time.sleep(1)
