import datetime
from time import strftime,gmtime

#botanswers

country = 'default'



def get_time3():
	today = datetime.date.today()
	return (str(today.strftime('Today is %d %b %Y.')))

def get_time2():
	return (strftime('Time in GMT: %H:%M:%S', gmtime()))

answers = {
'.hbot':'Welcome to hohilbot, this message is really helpful.',
'.habout':'This bot is completely random because it might work but also might not.',
'.hdate':get_time3(),
'.htimeK':get_time2(),
'.ekb':'cuck and oligarch',
'.oligarch':'ekb',
'.jews':'shut it down goyims know'
}
