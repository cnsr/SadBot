import datetime
from time import strftime,gmtime
import random

#botanswers

country = 'default'
ball = ['it is certain', 'it is decidedly so', 'without a doubt', 'yes definitely',
            'you may rely on it', 'as i see, yes', 'most likely', 'outlook good', 'yes',
            'signs point to yes', 'reply hazy try again', 'ask again later', 'better not tell you now',
            'cannot predict now', 'concentrate and ask again', "don't count on it",
            'my reply is no', 'my sources say no', 'outlook not so good', 'very doubtful',
            'you should kill yourself', 'literally fuck off', 'how am i supposed to know', 'idk',
            'yeah, probably not', 'haha faggot no of course']


def get_time3():
	today = datetime.date.today()
	return (str(today.strftime('Today is %d %b %Y.')))


def get_time2():
	return (strftime('Time in GMT: %H:%M:%S', gmtime()))


answers = {
'^[.]hbot$': 'Welcome to hohilbot, this message is really helpful.',
'^[.]habout$': 'This bot is completely random because it might work but also might not.',
'^[.]hdate$': get_time3(),
'^[.]htimeK$': get_time2(),
'^[.]jews$': 'shut it down goyim know',
'^[.]hohol$': 'should kill himself tbh',
'^[.]re+': 'reeeeee',
}
