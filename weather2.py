import urllib, unicodedata
from PIL import image
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
        w, h = img.size
        img.crop(0, 0, w, h - 165)
        img.save('weather.png')

