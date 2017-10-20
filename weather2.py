import urllib, unicodedata
from PIL import Image
w = 'http://wttr.in/'

def weather(location, **kwargs):
    if 'murrica' in kwargs:
        temp = '_u'
    else:
        temp = '_m'
    if location:
        l = w + '~' + location.encode('utf-8').replace(' ', '+') + temp + '0Q' + '.png'
        urllib.urlretrieve(l, 'weather.png')
        img = Image.open('weather.png')
        width, h = img.size
        if not width - 165 < 200:
            img = img.crop((0, 0, width - 165, h))
        img.save('weather.png')

