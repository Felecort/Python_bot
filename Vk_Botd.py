
'''     Vk Bot
        V-1.9.21      '''

from Bot_Options import *


def Weather():
    try:
        response = get('https://geocode-maps.yandex.ru/1.x/',
            params={
                'apikey': '',
                'format': 'json',
                'geocode': cmd[1]
                     })
        coord = json.loads(response.content)['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos'].split(" ")
        data = get("http://api.openweathermap.org/data/2.5/find",
            params={
                'lang': 'ru',
                'lat': coord[1],
                'lon': coord[0],
                'appid': '',
                'units': 'metric'
                     })
        weather_data = json.loads(data.content)['list'][0]
        main = weather_data['main']
        message_bot = f"⚙: В городе {cmd[1]} сейчас {weather_data['weather'][0]['description']}\nТемпература в районе {round(main['temp'])}℃\nПо ощущениям {round(main['feels_like'])}℃\nВлажность около {main['humidity']}%\nСкорость верта = {weather_data['wind']['speed']}м/с"
        vk.messages.send(
            message=message_bot,
            peer_id=peer_id,
            random_id=randint(0, 100000))

    except:
        vk.messages.send(
            message='Такого города не существует',
            peer_id=peer_id,
            random_id=randint(0, 100000))


def Say():
    if len(cmd[1]) > 300:
        return vk.messages.send(
            message="⚙: Ваше сообщение превышает 300 символов",
            peer_id=peer_id,
            random_id=randint(0, 100000))
    tts = gTTS(cmd[1], lang="ru")
    tts.save('./data/voice.ogg')

    response = vk.uploader.document_message('./data/voice.ogg', peer_id=peer_id, doc_type='audio_message')
    audio_message = vk.uploader.format(response, "doc")
    vk.messages.send(
        message="⚙",
        peer_id=peer_id,
        attachment=audio_message,
        random_id=randint(0, 100000))


def Zalgo():
    message = Reply('text')
    if message == None or len(cmd) == 1:
        return None
    for i in range(int(cmd[1])):
        message = zg.zalgofy(message)
    vk.messages.send(
        message=message,
        peer_id=peer_id,
        random_id=randint(0, 100000))


def Action():
    reply_id = Reply('from_id')
    user_send = vk.users.get(user_id=from_id, fields='sex')['response'][0]
    user_reply = vk.users.get(user_id=reply_id, fields='first_name_acc')['response'][0]
    return from_id, user_send['first_name'], reply_id, user_reply['first_name_acc'], user_send['sex']


def Send(message, photo_id):
    vk.messages.send(
        message=message,
        peer_id=peer_id,
        attachment="photo-170249375_" + photo_id,
        random_id=randint(0, 100000))


def Startle():
    data = (Action())
    if data[4] == 1:
        Send("@id%s(%s) напугала деда @id%s(%s)" % (data[0], data[1], data[2], data[3]), '457239584')
    else:
        Send("@id%s(%s) напугал деда @id%s(%s)" % (data[0], data[1], data[2], data[3]), '457239584')


def Kill():
    data = (Action())
    if data[4] == 1:
        Send("@id%s(%s) убила  @id%s(%s)" % (data[0], data[1], data[2], data[3]), '457239584')
    else:
        Send("@id%s(%s) убил @id%s(%s)" % (data[0], data[1], data[2], data[3]), '457239584')

def Citation():
    try:
        message = message_obj['reply_message']['text']
        user_id = message_obj['reply_message']['from_id']
    except:
        message = message_obj['fwd_messages'][0]['text']
        user_id = message_obj['fwd_messages'][0]['from_id']

    user_info = vk.users.get(user_id=user_id, fields='photo_50')['response'][0]
    url_data = get(user_info['photo_50'])

    with open("./data/ava.jpg", "wb") as user_photo:
        user_photo.write(url_data.content)

    user_name = f"{user_info['first_name']}\n{user_info['last_name']}"
    message = "\n".join(wrap(message, 34))
    user_photo = Image.open('./data/ava.jpg')

    base = Image.open('./data/back.jpg').convert('RGBA')
    txt = Image.new('RGBA', base.size, (0, 0, 0, 0))

    ImageDraw.Draw(txt).text((150, 70), f"«{message}»", font=font_italic, fill=(255, 255, 255, 255))
    ImageDraw.Draw(txt).text((45, 300), user_name, font=font, fill=(255, 255, 255, 255))
    base.paste(user_photo, area)
    Image.alpha_composite(base, txt).save("./data/citation.png")

    response = vk.uploader.message_photo('./data/citation.png', peer_id=peer_id)
    photo = vk.uploader.format(response, type_obj="photo")
    vk.messages.send(
        message="⚙",
        attachment=photo,
        peer_id=peer_id,
        random_id=randint(0, 1000000))


def Information():
    vk.messages.send(
        message=f"Вероятность того, что {cmd[1]} cоставляет {randint(0, 110)}%",
        peer_id=peer_id,
        random_id=randint(0, 1000000))


def When():
    vk.messages.send(
        message="Примерно %s.0%s.%s %s" % (randint(1, 30), randint(1, 9), randint(2020, 2100), cmd[1]),
        peer_id=peer_id,
        random_id=randint(0, 1000000))


def Send_Image(owner_id, photo_list):
    vk.messages.send(
        attachment=f"photo{owner_id}_{choice(photo_list)}",
        peer_id=peer_id,
        random_id=randint(0, 1000000))


def Who():
    users = vk.messages.getConversationMembers(peer_id=peer_id)
    if 'error' in users:
        return vk.messages.send(
            message='Отсутствуют права администратора для просмотра списка участников',
            peer_id=peer_id,
            random_id=randint(0, 100000))
    user = choice(users["response"]['profiles'])
    id_random_user = user['id']
    name_random_user = user['first_name']
    vk.messages.send(
        message='Я думаю, что @id%s(%s) -- %s' % (id_random_user, name_random_user, cmd[1]),
        peer_id=peer_id,
        random_id=randint(0, 1000000))


def True_False():
    vk.messages.send(
        message=f"{cmd[1]} {choice([' - чистейшая правда', ' - наглая ложь'])}",
        peer_id=peer_id,
        random_id=randint(0, 1000000))


def Speech(link):
    url_data = get(link)

    with open("./data/voice_message.mp3", "wb") as audio_data:
        audio_data.write(url_data.content)

    song = AudioSegment.from_mp3("./data/voice_message.mp3")
    song.export("./data/voice_message.wav", format="wav")

    with AudioFile("./data/voice_message.wav") as source:
        audio = rec.record(source)

    try:
        voice_text = rec.recognize_google(audio, language='ru-RU')
        vk.messages.send(
            message=f"⚙: {voice_text}",
            peer_id=peer_id,
            random_id=randint(0, 100000))

    except:
        vk.messages.send(
            message='⚙: Ошибка при распозновании',
            peer_id=peer_id,
            random_id=randint(0, 100000))


def Transliterate(message):
    if message == None:
        return None
    for key in translit_list:
        message = message.replace(key, translit_list[key])
    vk.messages.send(
        message=message,
        peer_id=peer_id,
        random_id=randint(0, 100000))


def Helper():
    vk.messages.send(
        message=comands,
        peer_id=peer_id,
        random_id=randint(0, 100000))


def Reply(obj):
    if 'reply_message' in message_obj:
        return message_obj['reply_message'][obj]
    elif 'fwd_messages' in message_obj and message_obj['fwd_messages'] != []:
        return message_obj['fwd_messages'][0][obj]
    else:
        vk.messages.send(
            message='Необходимо переслать/ответить на сообщение пользователя',
            peer_id=peer_id,
            random_id=randint(0, 100000))

#sssss
def Spam():
    for i in range(100):
        vk.messages.send(
            message=spam * 62,
            peer_id=peer_id,
            random_id=randint(0, 100000))
        sleep(0.2)


def Convene():
    users = vk.messages.getConversationMembers(peer_id=peer_id)
    if 'error' in users:
        return vk.messages.send(
            message='Отсутствуют права администратора для просмотра списка участников',
            peer_id=peer_id,
            random_id=randint(0, 100000))
    users_ids = ['[id' + str(i["id"]) + '|\u200b]' for i in users["response"]['profiles']]
    vk.messages.send(
        message=f"Созыв всех участников беседы {''.join(users_ids)}",
        peer_id=peer_id,
        random_id=randint(0, 100000))


def Translate(mytext):
    if mytext == None:
        return None
    if len(cmd) > 1:
        text = get('https://translate.yandex.net/api/v1.5/tr.json/translate',
                   params={
                          "key": '',
                          "text": mytext,
                          "lang": 'ru-en'
                                         })
        message = text.json()["text"][0]
        return vk.messages.send(
            message=message,
            peer_id=peer_id,
            random_id=randint(0, 100000))
    text = get('https://translate.yandex.net/api/v1.5/tr.json/translate',
        params={
            "key": '',
            "text": mytext,
            "lang": 'en-ru'
                })
    message = text.json()["text"][0]
    return vk.messages.send(
        message=message,
        peer_id=peer_id,
        random_id=randint(0, 100000))



def Get_Chat_Admins():
    users = vk.messages.getConversationMembers(peer_id=peer_id)['response']['items']
    chat_admins = list(filter(None, [i['member_id'] if 'is_admin' in i else None for i in users]))
    return chat_admins


def Kick(user_id):
    if user_id == None:
        return None
    number = peer_ids_list.index(peer_id)
    chat_admins = bot_data[number]['admins']
    if from_id in chat_admins:
        vk.messages.removeChatUser(user_id=user_id, chat_id=peer_id-2000000000)


def Admin(whom_id):
    if whom_id == None:
        return None
    try:
        chat_admins = Get_Chat_Admins()
    except:
        return vk.messages.send(
            message='Необходимо выдать боту права администратора',
            peer_id=peer_id,
            random_id=randint(0, 100000))
    number = peer_ids_list.index(peer_id)
    bot_dict = bot_data[number]
    if from_id in chat_admins:
        if whom_id in bot_dict['admins']:
            return vk.messages.send(
                message='Пользователь уже является администратором',
                peer_id=peer_id,
                random_id=randint(0, 100000))
        bot_data[number]['admins'].append(whom_id)
        Base_Update(bot_data)
        return vk.messages.send(
            message=f'Теперь @id{whom_id}(пользователь) является администратором',
            peer_id=peer_id,
            random_id=randint(0, 100000))
    return vk.messages.send(
        message='Только администраторы беседы могут назначать администраторов',
        peer_id=peer_id,
        random_id=randint(0, 100000))


def Del_Admin(whom_id):
    if whom_id == None:
        return None
    try:
        chat_admins = Get_Chat_Admins()
    except:
        return vk.messages.send(
            message='Необходимо выдать боту права администратора',
            peer_id=peer_id,
            random_id=randint(0, 100000))

    number = peer_ids_list.index(peer_id)
    bot_dict = bot_data[number]
    if from_id in chat_admins:
        if whom_id in bot_dict['admins']:
            bot_data[number]['admins'].remove(whom_id)
            Base_Update(bot_data)
            return vk.messages.send(
                message=f'@id{whom_id}(пользователь) больше не является администратором',
                peer_id=peer_id,
                random_id=randint(0, 100000))
        return vk.messages.send(
            message='Пользователь не является администратором',
            peer_id=peer_id,
            random_id=randint(0, 100000))
    return vk.messages.send(
        message='Только администраторы беседы могут редактировать список администраторов Бота',
        peer_id=peer_id,
        random_id=randint(0, 100000))


def Add_peer_id():
    new_id = {
              'peer_id': peer_id,
              'black_list': [],
              'admins': [384150583]
             }
    bot_data.append(new_id)
    Base_Update(bot_data)
    peer_ids_list.append(peer_id)
    return vk.messages.send(
        message='Ваша беседа успешно зарегистрирована.\nДля корректной работы предоставьте права администратора',
        peer_id=peer_id,
        random_id=randint(0, 100000))


def Del_All_Admins_of_Chat():
    users = vk.messages.getConversationMembers(peer_id=peer_id, fields='can_kick')['response']['items']
    number = peer_ids_list.index(peer_id)
    bot_dict = bot_data[number]
    chat_admins = bot_dict['admins']
    for i in users:
        if 'is_owner' in i and i['member_id'] == from_id:
            bot_data[number]['admins'].clear()
            Base_Update(bot_data)
            return vk.messages.send(
                message='Список администраторов очищен',
                peer_id=peer_id,
                random_id=randint(0, 100000))
    return vk.messages.send(
        message='Только создатель беседы может очистить список администраторов',
        peer_id=peer_id,
        random_id=randint(0, 100000))


def Base_Update(bot_data):
    with open(file_name, 'w') as my_file:
        json.dump(bot_data, my_file, indent=4)
    with open(file_name, 'r') as my_file:
        bot_data = json.load(my_file)


print('Бот запущен')

while True:
    for event in vk.longpoll.listen():
        try:
            if event['type'] == 'message_new':
                message_obj = event['object']['message']
                message = message_obj['text']
                from_id = message_obj['from_id']
                peer_id = message_obj['peer_id']
                if peer_id not in peer_ids_list and peer_id > 2000000000:
                    Add_peer_id()
                    vk.messages.send(
                        message=peer_id,
                        peer_id=2000000006,
                        random_id=randint(0, 100000))
                cmd = message.split(" ", maxsplit=1)
                cmd[0] = cmd[0].lower()
                if message[:1] == '/' and from_id > 0:

                    if cmd[0] == '/погода':
                        Weather()

                    elif cmd[0] == "/инфа":
                        Information()

                    elif cmd[0] == "/когда":
                        When()

                    elif cmd[0] == "/скажи":
                        Say()

                    elif cmd[0] == '/залго':
                        Zalgo()

                    elif cmd[0] == '/цитата':
                        Citation()

                    elif cmd[0] in ['/правда', '/правда,']:
                        True_False()

                    elif cmd[0] == '/админ':
                        Admin(Reply('from_id'))

                    elif cmd[0] == '/-админ':
                        Del_Admin(Reply('from_id'))

                    elif cmd[0] == '/удалитьадминов':
                        Del_All_Admins_of_Chat()

                    elif cmd[0] == "/мем":
                        Send_Image(-103083994, photo_list_meme)

                    elif cmd[0] == "/эро":
                        Send_Image(-129067329, photo_list_ero)

                    elif cmd[0] == '/транслит':
                        Transliterate(Reply('text'))

                    elif cmd[0] == '/помощь':
                        Helper()

                    elif cmd[0] == '/кик':
                        Kick(Reply('from_id'))

                    elif cmd[0] == '/кто':
                        Who()

                    elif cmd[0] == '/убить':
                        Kill()

                    elif cmd[0] == '/напугать':
                        Startle()

                    elif cmd[0] == '/спам' and from_id == 384150583:
                        Spam()

                    elif cmd[0] == '/перевести':
                        Translate(Reply('text'))

                    elif cmd[0] == '/созвать':
                        Convene()

                    elif message[:2] == '//' and from_id == 384150583:
                        exec(cmd[1])

                elif message_obj["attachments"] and message_obj["attachments"][0]["type"] == "audio_message":
                    Speech(message_obj['attachments'][0]['audio_message']['link_mp3'])

        except Exception as error:
            if 'Flood control' in str(error):
                sleep(4)
            else:
                print(error)
            vk.messages.send(
                message=error,
                peer_id='',
                random_id=randint(0, 100000))
