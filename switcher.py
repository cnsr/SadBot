# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

symbols = (u"йцукенгшщзхъфывапролджэ\ячсмитьбю.",
            u"qwertyuiop[]asdfghjkl;'\zxcvbnm,./")

def switch(text):
    text = text.lower().replace(u'ї', u'ъ').replace(u'і', u'ы').replace(u'є', u'э').replace(u'ґ', u'\\')
    tr = dict([(ord(a), ord(b)) for (a, b) in zip(*symbols)])
    return text.translate(tr)

def switchback(text):
    tr = dict((v, k) for k, v in (dict([(ord(a), ord(b)) for (a, b) in zip(*symbols)])).iteritems())
    return text.lower().translate(tr).encode('utf-8')

