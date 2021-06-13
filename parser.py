import requests
from bs4 import BeautifulSoup

URL = 'http://www.volgograd.ru/news/'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/91.0.4472.77 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9'}
HEADERS_WITH_HOST = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/91.0.4472.77 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9',
    'host' : 'www.volgograd.ru'}


def get_html(url, params=None):
    req = requests.get(url, headers=HEADERS, params=params)
    return req

def get_html_child(url) :
    req = requests.get(url, headers=HEADERS_WITH_HOST)
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
    print(news_items)


def get_news_text(url):
    html = get_html_child(url)

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
        get_content(html.text)
    else:
        print('ERROR: cant find url')


parse()
