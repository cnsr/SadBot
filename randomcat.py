import requests, re, json, urllib


def cat():
    url = 'http://random.cat/meow'
    r = requests.get(url)
    x = json.loads(r.text)
    link = x['file']
    ext = link.split('.')[-1]
    extreturn = 'kot.' + ext
    urllib.urlretrieve(link, extreturn)
    return extreturn

