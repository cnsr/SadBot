import requests, re, json, urllib

api = 'https://min-api.cryptocompare.com/data/'
base = 'https://www.cryptocompare.com'

def crypto(curr):
    curr = curr.upper()
    try:
        r = requests.get(api + 'price?fsym=' + curr + '&tsyms=BTC,USD,EUR')
        x = json.loads(r.text)
        if not 'Response' in x:
            answer = '1 ' + curr + ' is worth:'
            for k, v in x.iteritems():
                if k != curr:
                    answer += '\n' + str(v) + ' ' + k
            return answer
    except:
        pass

