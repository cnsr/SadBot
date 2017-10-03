import random, requests, urllib
from bs4 import BeautifulSoup as bs


def cat():
    imgur_link = 'https://imgur.com'
    cats = 'https://imgur.com/r/cats'
    r = requests.get(cats)
    soup= bs(r.text, 'lxml')
    links = soup.findAll('a', {'class': 'image-list-link'})
    hrefs = []
    for x in links:
        hrefs.append(x['href'])
    random.shuffle(hrefs)
    r2 = requests.get(imgur_link + random.choice(hrefs))
    soup2 = bs(r2.text, 'lxml')
    kit = 'https:' + soup2.find('a', {'class': 'zoom'})['href']
    ext = kit.split('.')[-1]
    extreturn = 'kit.' + ext
    urllib.urlretrieve(kit, extreturn)
    return extreturn

