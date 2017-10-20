import requests, re, json, urllib, random

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
                    if 'e' in str(v):
                        v = "{:.8f}".format(float(v))
                    answer += '\n' + str(v) + ' ' + k
            return answer
    except:
        pass


def money(m):
    amount = c1 = c2 = None
    if m:
        amount = m[0]
        c1 = m[1]
        try:
            if len(m) == 4:
                c2 = m[3]
            else:
                if m[2]:
                    c2 = m[2]
        except:
            pass
    try:
        r = api + 'price?fsym=' + c1 + '&tsyms='
        if c2 and c1 != c2:
            r = r + c2
        else:
            r = r + 'USD,EUR,GBP,RUB,UAH'
        req = requests.get(r)
        x = json.loads(req.text)
        if not 'Response' in x:
            answer = str(amount) + ' ' + c1 + ' is worth'
            for k, v in x.iteritems():
                if k != c1:
                    v = int(amount) * v
                    if 'e' in str(v):
                        v = "{:.8f}".format(float(v))
                    answer += '\n' + str(v) + ' ' + k
            return answer
    except:
        return 'Error occured. Make sure you entered request in format ".m (amount) currency (to/in) (currency2)))"'


def detailed(curr):
    curr = curr.upper()
    answer = 'Data on ' + curr + '/USD from CCCAGG:'
    link = 'https://www.cryptocompare.com/api/data/coinsnapshot/?fsym=' + curr + '&tsym=USD'
    try:
        r = requests.get(link)
        x = json.loads(r.text)
        pick = x['Data']["AggregatedData"]
        for k, v in pick.iteritems():
            for x in ['PRICE', 'OPEN24HOUR', 'HIGH24HOUR', 'LOW24HOUR',]:
                if str(k) == str(x):
                    answer = answer + '\n' + str(k) + ' ' + str(v)
        return answer
    except:
        pass

