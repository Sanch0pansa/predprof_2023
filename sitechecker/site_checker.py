import urllib.request
from time import time


def opening_time(website):
    open_time = time()
    website.read()
    close_time = time()
    website.close()
    return (close_time - open_time)


def check(urls):
    statuses = []
    for url in urls:
        website = urllib.request.urlopen(url)
        statuses.append(website.getcode() == 200 and
                        opening_time(website) < 3)
    return statuses


print(check(['https://fedingo.com/python-script-to-check-url-status/']))
