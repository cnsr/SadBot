from yandex_translate import YandexTranslate
key = 'trnsl.1.1.20171020T152455Z.1db5c3cb2da8bd85.c38b274bffe7fbf4fa26170fdd306c88a36c874f'
t = YandexTranslate(key)

def translate(text):
    lang = t.detect(text)
    if lang != 'en':
        translation = t.translate(text, 'en')['text'][0]
        answer = 'translated from ' + lang + ':\n' + translation
        return answer

