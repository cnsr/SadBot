from gtts import gTTS as g
from yandex_translate import YandexTranslate
key = 'trnsl.1.1.20171020T152455Z.1db5c3cb2da8bd85.c38b274bffe7fbf4fa26170fdd306c88a36c874f'
t = YandexTranslate(key)

def tts(text):
    lang = t.detect(text)
    tts = g(text=text, lang=lang, slow=True)
    tts.save('tts.ogg')

