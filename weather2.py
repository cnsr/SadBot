import urllib

w = 'http://wttr.in/'

def weather(location):
    if location:
        l = w + '~' + location.replace(' ', '+') + '_0.png'
        urllib.urlretrieve(l, 'weather.png')

