import signal
import threading
import time
import requests

from datetime import timedelta
from bs4 import BeautifulSoup
from pymongo import MongoClient

WAIT_TIME_SECONDS = 20


class Job(threading.Thread):
    def __init__(self, interval, execute, *args, **kwargs):
        threading.Thread.__init__(self)
        self.daemon = False
        self.stopped = threading.Event()
        self.interval = interval
        self.execute = execute
        self.args = args
        self.kwargs = kwargs

    def stop(self):
        self.stopped.set()
        self.join()

    def run(self):
        while not self.stopped.wait(self.interval.total_seconds()):
            self.execute(*self.args, **self.kwargs)


class ProgramKilled(Exception):
    pass


def signal_handler(signum, frame):
    raise ProgramKilled


URL = 'http://www.volgograd.ru/news/'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/91.0.4472.77 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9'}


def get_html(url, params=None):
    req = requests.get(url, headers=HEADERS, params=params)
    return req


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    news = soup.findAll('div', class_='news-item')
    news_items = []
    for new in news:
        ref = URL
        ref_to_news = new.find('a').get('href')
        if ref_to_news.__contains__('gubernator'):
            ref = ref[:-6] + ref_to_news
        else:
            ref += ref_to_news[6:]

        news_items.append({
            'title': new.find('a').text,
            'ref': ref,
            'date': new.find('div', class_='date').text,
            'text': get_news_text(ref)
        })

    # print(news_items)
    return news_items


def get_news_text(url):
    html = get_html(url)

    if html.status_code == 200 or html.status_code == 304:
        soup = BeautifulSoup(html.text, 'html.parser')
        text = soup.find('div', class_='news-detail')
        text = text.findAll('p')

        result = ''
        for item in text:
            result += item.get_text()

        escapes = ''.join([chr(char) for char in range(1, 32)])
        translator = str.maketrans('', '', escapes)
        result = result.translate(translator)
        return result
    else:
        return 'Cant find child url'


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        content = get_content(html.text)
        client = MongoClient('mongodb://localhost:27017/?ssl=false')
        db = client.NewsData
        counter = 0
        news_added = 0
        for item in content:
            if db.News.count_documents({'ref': item['ref']}, limit=1) > 0:
                continue
            result = db.News.insert_one(item)
            print('Inserted {0} as {1}'.format(counter, result.inserted_id))
            counter += 1
            news_added += 1
        print('Added {0} items in database'.format(news_added))
    else:
        print('ERROR: cant find url')


if __name__ == "__main__":
    periodicity = int(input('Input update periodicity in seconds : '))

    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    job = Job(interval=timedelta(seconds=periodicity), execute=parse)
    job.start()
    while True:
        try:
            time.sleep(1)
        except ProgramKilled:
            print("Program killed")
            "Program killed"
            job.stop()
            break
