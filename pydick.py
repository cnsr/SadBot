from PyDictionary import PyDictionary
d = PyDictionary()

def meaning(word):
    answer = ''
    try:
        m = d.meaning(word)
        for k, v in m.iteritems():
            answer += '[b]' +  k + ':[/b] '
            for x in v:
                answer += x + '\n'
    except Exception as e:
        answer = 'no such word'
    return answer

