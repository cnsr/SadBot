#remade by cnsr based on livechan API and anna bot code
#added telegram integration
###bot starts receiving incoming data only after sending any outcoming message
#kinda works but not really

#imports
from time import sleep
from api import *
import telebot
import re
import sys
import random
import config
from urllib2 import urlopen
import hbot
import requests
import pyowm

import users_dict

import urllib
from bs4 import BeautifulSoup, Comment

tbot = telebot.TeleBot(config.token)

#if you don't input channel to connect to'
if (len(sys.argv) < 2):
	print("Usage: python bot.py [channel]")
	exit()

#if you did it just werks
channel = sys.argv[1]

#writes image on disk so it could be readen by api later
def send_image(url):
	url = url.replace('/home/ph/livechan-js/public/',
	'https://sadchan.sytes.net/')
	f = open('out.jpg','wb')
	f.write(urllib2.urlopen(url).read())
	f.close()

#used to check if user exists in separate file so you could add him if he doesnt
def write_in(txt,txt1,txt2):
	with open('users.txt','a') as f:
		f.write('\n' + txt + ' - ' + txt1 + ' - ' + txt2)

base_url = 'http://www.worldtimeserver.com/current_time_in_'

class Opener(urllib.FancyURLopener):
	version = 'App/1.7'

def process_chat(*args):
	#uncomment for debug:
	#print(args)
	#just to ease finding this block in code
	try:
		#get vars from args
		ident = args[0]["identifier"]
		message = args[0]["body"]
		name = args[0]["name"]
		count = str(args[0]["count"])
		convo = args[0]["convo"]
		country_name = args[0]["country_name"]
		country = args[0]["country"]
		
		#print(country)	
		#print(ident)
		
		def get_time():
			c = ''
			result = ''
			result_time = ''
			for char in country:
				if char.isalpha():
					c += char
			c = c[:2]
			url = base_url + c + '.aspx'	
			r = Opener().open(url)
			soup = BeautifulSoup(r,'lxml')
			#gets time
			time_comments = soup.findAll(text=lambda text:isinstance(text,Comment))
			for x in time_comments:
				y = ''
				for char in x:
					if char != ' ':
						y += char
				if re.match('ServerTimewithseconds:',y):
					result = y
			for char in result:
				if not char.isalpha():
					result_time += char
			result_time = result_time[1:]
			#gets city + country
			city_found = soup.find('h1',{'class':'placeNameH1'})
			city = city_found.text
			#cleaning up city output
			city = re.sub('\s+','',city)
			city = ' '.join(re.findall('[A-Z][^A-Z]*',city))
			#prints result
			return ('Time in {0} is {1}'.format(city, result_time))
		
		
		help_msg = 'no help message defined'
		
		#for those who don't have names
		if name == '' or name == 'Anonymous' or len(name) == 1:
			if ident not in users_dict.users:
				name = "<-" + country + '->'
			else:
				name = users_dict.users[ident]
		
		#gets weather, sometimes off
		wreq = re.compile('\.hweather( (.+))?').match(message)
		if wreq:
			answer = ''
			try:
				wr = wreq.group(2)
				# setting up weather
				random.shuffle(config.weatherapikeys)
				apikey = random.choice(config.weatherapikeys)
				owm = pyowm.OWM(apikey)
				obs = owm.weather_at_place(wr)
				w = obs.get_weather()
				#gets all variables
				location = obs.get_location()
				loc = location.get_name()
				tempC = w.get_temperature('celsius')
				tempF = w.get_temperature('fahrenheit')
				tC = str(tempC['temp'])
				tF = str(tempF['temp'])
				hum = str(w.get_humidity())
				status = w.get_detailed_status()
				answer = ('Weather in {0}:\ntemperature: {1}C, {2}F\n\
humidity: {3}%\nweather: {4}').format(loc, tC, tF, hum, status)
			except Exception as e:
				print(e)
				answer = 'error occured while parsing your request, check spelling'
			out_msg = '>>' + count + '\n' + answer
			post_chat(out_msg, channel, name = config.name,trip = config.Trip,convo = 'General', file = '')
		
		#gets time
		#THIS DOESNT FUCKING WORK IN A SEPARATE FILE
		if re.match(message,'.htime') and message !='':
			out_msg = out_msg = '>>' + count + '\n' + get_time()
			post_chat(out_msg, channel, name = config.name,trip = config.Trip,convo = 'General', file = '')
		
		#bot commands
		#YES STEF THIS IS THE WAY IT SHOULD FUCKING BE NO FUCKING CALLBACK FUNCS
		for (k,v) in hbot.answers.iteritems():
			if re.match(k,message):
				help_msg = hbot.answers[k]
				out_msg = '>>' + count + '\n' + help_msg
				post_chat(out_msg, channel, name = config.name,trip = config.Trip,convo = 'General', file = '')
				
		#handles text messages only, text + photo will only be handled as photo by next handler
		@tbot.message_handler(func=lambda incM: True)
		def handle_text(incM):
			post_chat(incM.text, channel, name = config.name,trip = config.Trip, convo="General",file = '')
		
		#only handles photos, doesnt work with text
		@tbot.message_handler(content_types=['photo','text'])
		def handle_image(message):
			file_id = message.photo[-1].file_id
			imageIn = tbot.get_file(file_id)
			image_file = requests.get('https://api.telegram.org/file/bot' + config.token + '/' + imageIn.file_path)
			with open('in.jpg','wb') as f:
				f.write(image_file.content)
			post_chat('',channel, name=config.name,trip = config.Trip, convo = 'General', file = 'in.jpg')
		
		#only sends posts from 'General' conversation
		if convo == "General":
			if "image" in args[0].keys():
				out_image = args[0]["image"]
			else:
				out_image = ''
			
			msg = name + ":\n" + message
			
			#this doesnt work smh
			subname = config.name.split('#');
			if name != config.name and name != subname[0]:
				if out_image != '':
					send_image(out_image)
					img = open('out.jpg', 'rb')
					tbot.send_photo(config.user_id, img)
					img.close()
				tbot.send_message(config.user_id, msg)
				print(msg)
				
	except Exception as e:
		print(e)
		
#i guess this is better to have than not to?		
try:	
	login(callback=process_chat)
	join_chat(channel)
	print('Joined chat')
	#init msg to make bot work
	tbot.send_message(config.user_id, 'Joined chat.')
except Exception as e:
	print("Connection failed. Error message:")
	print(e)

#makes bot work and tbot polls endlessly(at least while no errors occure)
while 1:
	sleep(3)
	tbot.polling(none_stop = True)
