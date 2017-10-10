import urllib, unicodedata

w = 'http://wttr.in/'

def weather(location, **kwargs):
    if 'murrica' in kwargs:
        temp = '_u'
    else:
        temp = '_m'
    if location:
        l = w + '~' + location.encode('utf-8').replace(' ', '+') + temp + '0Q' + '.png'
        # print(l)
        urllib.urlretrieve(l, 'weather.png')

