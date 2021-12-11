import requests
from bs4 import BeautifulSoup


def quote_better():
    url = 'http://api.forismatic.com/api/1.0/'
    payload = {'method': 'getQuote', 'format': 'json', 'lang': 'ru'}
    r = requests.get(url, params=payload)

    data = r.json()
    quote = data['quoteText']
    author = data['quoteAuthor']

    if author != '':
        author = '© ' + author
    result = quote + "\n" + author
    return result


def quote_generator():
    r = requests.get("https://socratify.net/quotes/random")
    text = r.text

    soup = BeautifulSoup(text, 'lxml')
    quote = soup.select('h1.b-quote__text')[0].text.strip()
    author_dirty = soup.select('h2.b-quote__category')[0].text.strip().split(",")[0]
    author = author_dirty.replace(u'—\xa0\n                \n                    ', u'')

    if author == 'Неизвестный автор':
        author = ''
    else:
        author = '© ' + author
    result = quote + "\n" + author
    return result

