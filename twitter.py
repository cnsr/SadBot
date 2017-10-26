# -*- coding: utf-8 -*-
import tweepy, json, random, re, requests, urllib


CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_KEY = ''
ACCESS_SECRET = ''


auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

tag = '#ねこの写真ヘタクソ選手権'

def kat():
    tweets = tweepy.Cursor(api.search, q=tag).items(50)
    tweets_list = []
    for x in tweets:
        tweets_list.append(x)
    try:
        t = random.choice(tweets_list)
        tweet = json.dumps(t._json, indent=4)
        tj = json.loads(tweet)
        url = tj['entities']['media'][0]['media_url_https']
        ext = url.split('.')[-1]
        extreturn = 'kat.' + ext
        urllib.urlretrieve(url, extreturn)
        return extreturn
    except:
        pass


