# remade by cnsr based on livechan API and anna bot code
# added telegram integration
# bot starts receiving incoming data only after sending any outcoming message
# kinda works but not really

# imports
from time import sleep
from api import *
import os
import telebot
import re
import sys
import random
import config
from urllib2 import urlopen
import hbot
import requests
import pyowm
import urllib
from bs4 import BeautifulSoup, Comment
from randomcat import cat as rkot
from imgur import cat as rkit
from twitter import kat as rkat
import weather2 as wttr
from crypto import crypto, money, detailed
from htranslate import translate as ht
from tts import tts
from switcher import switch, switchback
tbot = telebot.TeleBot(config.token)
nsfw = False

# loads region codes
regioncodes = json.load(open('regioncodes.json'))

# if you don't input channel to connect to
if len(sys.argv) < 2:
    print("Usage: python bot.py [channel]")
    exit()
# if you did it just werks
channel = sys.argv[1]

# if nswf doesnt send the images
try:
    if sys.argv[2] == 'nsfw':
        nsfw = True
        print('NSFW is on!')
except IndexError:
    print('NSFW is off!')


# writes image on disk so it could be read by api later
def send_image(url):
    url = url.replace('/home/ph/livechan-js/public/',
                      'https://kotchan.org/')
    f = open('out.jpg', 'wb')
    f.write(urllib2.urlopen(url).read())
    f.close()


def send_file(url, extension):
    url = url.replace('/home/ph/livechan-js/public/',
                      'https://kotchan.org/')
    f = open('out' + extension, 'wb')
    f.write(urllib2.urlopen(url).read())
    f.close()


base_url = 'http://www.worldtimeserver.com/current_time_in_'


class Opener(urllib.FancyURLopener):
    version = 'App/1.7'


def process_chat(*args):
    # uncomment for debug:
    # print(args)
    try:
        # get vars from args
        ident = args[0]["identifier"]
        message = args[0]["body"]
        name = args[0]["name"]
        count = str(args[0]["count"])
        convo = args[0]["convo"]
        country_name = args[0]["country_name"]
        country = args[0]["country"]
        # checks if file exists an gets the extension of it
        if "image" in args[0].keys():
            extension = os.path.splitext(args[0]["image"])[-1].lower()
        else:
            extension = ''

        # scrapes and returns a random cat image/gif from random.cat
        if re.match('^[.]kit$', message):
            msg = '>>' + count
            f = random.choice([rkot, rkit, rkot, rkat])()
            post_chat(msg, channel, name=config.name, trip=config.Trip, convo='General', file=f)

        # returns one of many 8ball messages
        if re.match('^[.]8ball', message):
            random.shuffle(hbot.ball)
            mesg = random.choice(hbot.ball)
            post_chat('>>' + count + '\n' + mesg, channel, name=config.name, trip=config.Trip, convo='General', file='')

        # matches cryptocurrencies, returns their data
        if re.match('^[#][a-zA-Z]+$', message):
            msg = detailed(message[1:])
            if msg:
                post_chat('>>' + count + '\n' + msg, channel, name=config.name, trip=config.Trip, convo='General', file='')

        # matches crypto but just returns price data
        if re.match('^[$][a-zA-Z]+$', message):
            msg = crypto(message[1:])
            if msg:
                post_chat('>>' + count + '\n' + msg, channel, name=config.name, trip=config.Trip, convo='General', file='')

        # returns punto switcher-like string if someone fucked up and typed in russian
        sreq = re.compile('\.(sw|switch) ([\s\S]+)').match(message)
        if sreq:
            msg = switch(sreq.group(2))
            if msg:
                post_chat('>>' + count + '\n' + msg, channel, name=config.name, trip=config.Trip, convo='General', file='')

        # same but from english
        ssreq = re.compile('\.(bs|bswitch) ([\s\S]+)').match(message)
        if ssreq:
            msg = switchback(ssreq.group(2))
            if msg:
                post_chat('>>' + count + '\n' + msg, channel, name=config.name, trip=config.Trip, convo='General', file='')


        # in case it fucks up and sends empty message 
        help_msg = 'no help message defined'

        # money getter
        mreq = re.compile('\.(m|money )(.+)').match(message)
        if mreq:
            try:
                m = mreq.group(2).upper().split(' ')
                if not m[0].isnumeric():
                    m = [1] + m
                msg = money(m)
                if msg:
                    post_chat('>>' + count + '\n' + msg, channel, name=config.name, trip=config.Trip, convo='General', file='')
            except Exception as e:
                print(e)


        # gets weather, sometimes off
        # could be cleaned up but i won't bother right now
        wreq = re.compile('\@(weather|w)( (.+))?').match(message)
        if wreq:
            try:
                w = wreq.group(2)
                if not w:
                    w = regioncodes[country]
                if re.match('us', country[:2].lower()):
                    wttr.weather(w, murrica=False)
                else:
                    wttr.weather(w)
                msg = 'Weather in ' + w
                post_chat('>>' + count + '\n' + msg, channel, name=config.name, trip=config.Trip,
                      convo='General', file='weather.png')
            except Exception as e:
                print(str(e))

        # translates text into english
        treq = re.compile('(\.t )([\s\S]+)').match(message)
        if treq:
            try:
                msg = ht(treq.group(2))
                post_chat('>>' + count + '\n' + msg, channel, name=config.name, trip=config.Trip, convo='General', file='')
            except Exception as e:
                print(str(e))

        ttsreq = re.compile('([.]tts )([\s\S]+)').match(message)
        if ttsreq:
            try:
                tts(ttsreq.group(2))
                post_chat('>>' + count, channel, name=config.name, trip=config.Trip, convo='General', file='tts.ogg')
            except Exception as e:
                print(str(e))



        # checks messages for bot commands
        for (k, v) in hbot.answers.iteritems():
            if re.match(k, message):
                help_msg = hbot.answers[k]
                out_msg = '>>' + count + '\n' + help_msg
                post_chat(out_msg, channel, name=config.name,
                        trip=config.Trip,convo='General', file='')

        # handles text messages only, text + photo will only be handled as photo by next handler
        @tbot.message_handler(func=lambda incM: True)
        def handle_text(incM):
            post_chat(incM.text, channel, name=config.name, trip=config.Trip,
                      convo="General", file='')

        # only handles photos, doesnt work with text
        @tbot.message_handler(content_types=['photo', 'text'])
        def handle_image(message):
            file_id = message.photo[-1].file_id
            imageIn = tbot.get_file(file_id)
            image_file = requests.get('https://api.telegram.org/file/bot' + config.token + '/' + imageIn.file_path)
            with open('in.jpg', 'wb') as f:
                f.write(image_file.content)
            post_chat('', channel, name=config.name,
                      trip=config.Trip, convo='General', file='in.jpg')

        # only sends posts from 'General' conversation
        if convo == "General":
            if "image" in args[0].keys():
                out_image = args[0]["image"]
                if args[0]["image_filename"].startswith('anna'):
                    out_image = ''
            else:
                out_image = ''

            msg = str(count) + '| ' + name + ' | ' + country + " :\n" + message

            # this doesnt work smh
            try:
                if extension != '.webm':
                    tbot.send_message(config.user_id, msg)
                # will only send images if they exist and nsfw is off
                if out_image != '' and not nsfw and extension != '':
                    if extension not in ['.webm', '.gif', '.ogg', '.mp3', '.mp4']:
                        send_image(out_image)
                        img = open('out.jpg', 'rb')
                        tbot.send_photo(config.user_id, img)
                        img.close()
                    if extension == '.ogg':
                        send_file(out_image, extension)
                        ogg = open('out.ogg', 'rb')
                        tbot.send_voice(config.user_id, ogg)
                        ogg.close()
                    if extension == '.gif':
                        send_file(out_image, extension)
                        gif = open('out.gif', 'rb')
                        tbot.send_document(config.user_id, gif)
                        gif.close()
                    if extension == '.mp4':
                        send_file(out_image, extension)
                        video = open('out.mp4', 'rb')
                        tbot.send_video(config.user_id, video)
                        video.close()
                    if extension == '.webm':
                        url = args[0]['image'].replace('/home/ph/livechan-js/public/', 'https://kotchan.org/')
                        msg += '\n' + url
                        tbot.send_message(config.user_id, msg)


            except Exception as e:
                ree = '----------\n' + str(e) + '\n-----------'
                tbot.send_message(config.user_id, ree)
    except Exception as e2:
        print('Exception e2: ' + str(e2))
        print(args[0])

# i guess this is better to have than not to?
while True:
    try:
        login(callback=process_chat)
        join_chat(channel)
        print('Joined chat')
        # init msg to make bot work
        # it doesnt smh lel
        tbot.send_message(config.user_id, 'Joined chat.')
    except Exception as e:
        print("Connection failed. Error message:")
        print(e)
        pass
    else:
        break

# makes bot work and tbot polls endlessly(at least while no errors occur)
# and they do a lot
while 1:
    try:
        sleep(3)
        tbot.polling(none_stop=True)
    except:
        pass

