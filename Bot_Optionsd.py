
from PIL import Image, ImageDraw, ImageFont
from textwrap import wrap
from saya import Vk
from gtts import gTTS
from pydub import AudioSegment
from time import sleep, time
from random import randint, choice
from requests import get
from speech_recognition import Recognizer, AudioFile
from zalgo_text import zalgo
import json

group_id = 'your group id'
zg = zalgo.zalgo()
rec = Recognizer()
vk = Vk(token="", group_id=group_id)
vk_user = Vk(token="")

file_name = 'bot_data.json'
area = (45, 250, 95, 300)
font_italic = ImageFont.truetype('./data/a_Futurica_ExtraBoldItalic.ttf', 23)
font = ImageFont.truetype('./data/a_Futurica_ExtraBold.ttf', 18)
peer_ids_list = []

album_meme = vk_user.photos.get(owner_id=-103083994, album_id="wall", count=1000)["response"]["items"]
photo_list_meme = [i["id"] for i in album_meme]
del(album_meme)

spam = '👺❤💘🌵🐡🌚😅😜💮🧟‍♂🦸‍♀🙇‍♂🙆‍♂🌳🦑🌺🐉🥳😘📢🤠🥳😎'

comands = """
V-1.9.20
Распознование речи в войсах по умолчанию включено

## Основные команды ##
/помощь - список команд
/погода *город* - определение погоды на данный момент в городе
/инфа *событие* - рандомная вероятность события
/когда *событие* - рандомная дата события
/скажи *текст* - озвучка любого текста(в том числе и смайлов)
/правда *утверждение* - явяется ли утверждение правдой или ложью
/мем - рандомный мем
/кто *утверждение* - упомянание рандомного человека + утверждение
/созвать - созыв участников беседы
\n
## Кoманды, для которых необходимо   ##
## ответить на сообщение (переслать) ##
/транслит  - транслитерация раскладки сообщения
/перевести англ  - перевод сообщения с рус на англ
/перевести - перевод сообщения с англ на рус
/залго *степень заспамленности текста(число)* - преобразование в залго-текст

## Функции Чат-менеджера ##
/кик - кик юзера
/админ - назначение участника администратором
/-админ - удаление участника из списка администраторов
/удалитьадминов - полная очистка списка администраторов

\n
## Команды в разработке ##
/мут - удаление всех сообщений пользоваеля

## Другое ##
//*Python код* - выполнение Пайтон кода(доступно только гл. админам бота)"""

translit_list = {
                'q': 'й',
                'w': 'ц',
                'e': 'у',
                'r': 'к',
                't': 'е',
                'y': 'н',
                'u': 'г',
                'i': 'ш',
                'o': 'щ',
                'p': 'з',
                '[': 'х',
                ']': 'ъ',
                'a': 'ф',
                's': 'ы',
                'd': 'в',
                'f': 'а',
                'g': 'п',
                'h': 'р',
                'j': 'о',
                'k': 'л',
                'l': 'д',
                ';': 'ж',
                "'": 'э',
                'z': 'я',
                'x': 'ч',
                'c': 'с',
                'v': 'м',
                'b': 'и',
                'n': 'т',
                'm': 'ь',
                ',': 'б',
                '.': 'ю',
                '/': '.',
                '?': ',',
                '`': 'ё'
                        }


with open(file_name, 'r') as my_file:
    bot_data = json.load(my_file)
    peer_ids_list = [i["peer_id"] for i in bot_data]
