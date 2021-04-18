# импортируем библиотеки
from flask import Flask, request
import logging
import os
import random
import requests

# библиотека, которая нам понадобится для работы с JSON
import json
variant = ["Да", "Нет"]
cities = {
    'москва': '1030494/ab1be0709fd9b964e7a4',
    'казань': '1652229/0ecfd27f9f2b75480eb4',
    'йошкар-ола': '997614/6a4dc48e18dbc38dfadd',
    'псков': '997614/ba864fed76b4d2a6d993',
    'санкт-питербург': '1652229/bf46602baccff38a67e6',
    'красноярск': '997614/77c6afb95565e7212dc3',
    'уфа': '1652229/3f81b56a44f1ecaccc28',
    'ростов': '213044/f464bf5532b66326f5b0',
    'челябинск': '213044/6126144f4c2786fddfd4',
    'екатеринбург': '1540737/7aa33537943d51f198e4',
    'новосибирск': '1521359/9ae00b97c27b73dec3a0'


}
ist = ["Я угадываю событие", "Я угадываю дату"]
dat1 = {"1941": "начало великой отечественной войны", "1945": "завершение великой отечественной войны",
        "862":"призвание рюрика", "882": "князь олег захватил киев", "988":"принятие христианства",
        "1242":"ледовое побоище", "1240": "невская битва", "1380":"куликовская битва",
        "1812":"отечественная война с наполеоном"}

sob = {"начало великой отечественной войны": "1941", "завершение великой отечественной войны": "1945",
       "призвание рюрика":"862", "князь олег захватил киев":"882", "принятие христианства":"988",
       "ледовое побоище":"1242",  "невская битва":"1240", "куликовская битва":"1380",
        "отечественная война с наполеоном":"1812"}

dat = ["1941", "1945", "862", "882", "988", "1242", "1240", "1380", "1812"]

sob1 = ["начало великой отечественной войны", "завершение великой отечественной войны", "призвание рюрика",
        "князь олег захватил киев", "принятие христианства","ледовое побоище",  "невская битва", "куликовская битва",
        "отечественная война с наполеоном"]

cit = ['москва', 'казань', 'йошкар-ола', 'псков', 'санкт-питербург', 'красноярск', 'уфа', 'ростов', 'челябинск',
       'екатеринбург', 'новосибирск']
sit = ""
s = ''
sd = ''
# создаем словарь, где для каждого пользователя
# мы будем хранить его имя
sessionStorage1 = {}

town=["Абакан", "Азов", "Александров", "Алексин", "Альметьевск", "Анапа", "Ангарск", "Анжеро-Судженск",
      "Апатиты", "Арзамас", "Армавир", "Арсеньев", "Артем", "Архангельск", "Асбест", "Астрахань", "Ачинск", "Балаково",
      "Балахна", "Балашиха", "Балашов", "Барнаул", "Батайск", "Белгород", "Белебей", "Белово",
      "Белогорск", "Белорецк", "Белореченск", "Бердск", "Березники",
      "Березовский", "Бийск", "Биробиджан", "Благовещенск", "Бор",
      "Борисоглебск", "Боровичи", "Братск", "Брянск", "Бугульма", "Буденновск", "Бузулук", "Буйнакск", "Великие Луки",
      "Великий Новгород", "Верхняя Пышма", "Видное", "Владивосток", "Владикавказ", "Владимир", "Волгоград",
      "Волгодонск",
      "Волжск", "Волжский", "Вологда", "Вольск", "Воркута", "Воронеж", "Воскресенск", "Воткинск", "Всеволожск",
      "Выборг",
      "Выкса", "Вязьма", "Гатчина", "Геленджик", "Георгиевск", "Глазов", "Горно-Алтайск", "Грозный", "Губкин",
      "Гудермес",
      "Гуково", "Гусь-Хрустальный", "Дербент", "Дзержинск", "Димитровград", "Дмитров", "Долгопрудный", "Домодедово",
      "Донской", "Дубна", "Евпатория", "Егорьевск", "Ейск", "Екатеринбург", "Елабуга", "Елец", "Ессентуки",
      "Железногорск", "Железногорск", "Жигулевск", "Жуковский", "Заречный",
      "Зеленогорск", "Зеленодольск", "Златоуст", "Иваново", "Ивантеевка", "Ижевск", "Избербаш", "Иркутск", "Искитим",
      "Ишим", "Ишимбай", "Йошкар-Ола", "Казань", "Калининград", "Калуга", "Каменск-Уральский", "Каменск-Шахтинский",
      "Камышин", "Канск", "Каспийск", "Кемерово", "Керчь", "Кинешма", "Кириши", "Киров",
      "Кирово-Чепецк", "Киселевск", "Кисловодск", "Клин", "Клинцы", "Ковров", "Когалым", "Коломна",
      "Комсомольск-на-Амуре",
      "Копейск", "Королев", "Кострома", "Котлас", "Красногорск", "Краснодар", "Краснокаменск", "Краснокамск",
      "Краснотурьинск", "Красноярск", "Кропоткин", "Крымск", "Кстово", "Кузнецк", "Кумертау", "Кунгур", "Курган",
      "Курск",
      "Кызыл", "Лабинск", "Лениногорск", "Ленинск-Кузнецкий", "Лесосибирск", "Липецк", "Лиски", "Лобня", "Лысьва",
      "Лыткарино", "Люберцы", "Магадан", "Магнитогорск", "Майкоп", "Махачкала", "Междуреченск", "Мелеуз", "Миасс",
      "Минеральные Воды", "Минусинск", "Михайловка", "Михайловск)", "Мичуринск", "Москва",
      "Мурманск",
      "Муром", "Мытищи", "Набережные Челны", "Назарово", "Назрань", "Нальчик", "Наро-Фоминск", "Находка",
      "Невинномысск",
      "Нерюнгри", "Нефтекамск", "Нефтеюганск", "Нижневартовск", "Нижнекамск", "Нижний Новгород", "Нижний Тагил",
      "Новоалтайск", "Новокузнецк", "Новокуйбышевск", "Новомосковск", "Новороссийск", "Новосибирск", "Новотроицк",
      "Новоуральск", "Новочебоксарск", "Новочеркасск", "Новошахтинск", "Новый Уренгой", "Ногинск", "Норильск",
      "Ноябрьск",
      "Нягань", "Обнинск", "Одинцово", "Озерск", "Октябрьский", "Омск", "Орел", "Оренбург",
      "Орехово-Зуево", "Орск", "Павлово", "Павловский Посад", "Пенза", "Первоуральск", "Пермь", "Петрозаводск",
      "Петропавловск-Камчатский", "Подольск", "Полевской", "Прокопьевск", "Прохладный", "Псков", "Пушкино",
      "Пятигорск",
      "Раменское", "Ревда", "Реутов", "Ржев", "Рославль", "Россошь", "Ростов-на-Дону", "Рубцовск", "Рыбинск", "Рязань",
      "Салават", "Сальск", "Самара", "Санкт-Петербург", "Саранск", "Сарапул", "Саратов", "Саров", "Свободный",
      "Севастополь", "Северодвинск", "Северск", "Сергиев Посад", "Серов", "Серпухов", "Сертолово", "Сибай",
      "Симферополь",
      "Славянск-на-Кубани", "Смоленск", "Соликамск", "Солнечногорск", "Сосновый Бор", "Сочи", "Ставрополь",
      "Старый Оскол",
      "Стерлитамак", "Ступино", "Сургут", "Сызрань", "Сыктывкар", "Таганрог", "Тамбов", "Тверь", "Тимашевск",
      "Тихвин",
      "Тихорецк", "Тобольск", "Тольятти", "Томск", "Троицк", "Туапсе", "Туймазы", "Тула", "Тюмень", "Узловая",
      "Улан-Удэ", "Ульяновск", "Урус-Мартан", "Усолье-Сибирское", "Уссурийск", "Усть-Илимск", "Уфа", "Ухта",
      "Феодосия",
      "Фрязино", "Хабаровск", "Ханты-Мансийск", "Хасавюрт", "Химки", "Чайковский", "Чапаевск", "Чебоксары",
      "Челябинск",
      "Черемхово", "Череповец", "Черкесск", "Черногорск", "Чехов", "Чистополь", "Чита", "Шадринск", "Шали", "Шахты",
      "Шуя", "Щекино", "Щелково", "Электросталь", "Элиста", "Энгельс", "Южно-Сахалинск", "Юрга", "Якутск",
      "Ялта", "Ярославль"]

# мы передаём __name__, в нем содержится информация,
# в каком модуле мы находимся.
# В данном случае там содержится '__main__',
# так как мы обращаемся к переменной из запущенного модуля.
# если бы такое обращение, например,
# произошло внутри модуля logging, то мы бы получили 'logging'
app = Flask(__name__)

# Устанавливаем уровень логирования
logging.basicConfig(level=logging.INFO)

# Создадим словарь, чтобы для каждой сессии общения
# с навыком хранились подсказки, которые видел пользователь.
# Это поможет нам немного разнообразить подсказки ответов
# (buttons в JSON ответа).
# Когда новый пользователь напишет нашему навыку,
# то мы сохраним в этот словарь запись формата
# sessionStorage[user_id] = {'suggests': ["Не хочу.", "Не буду.", "Отстань!" ]}
# Такая запись говорит, что мы показали пользователю эти три подсказки.
# Когда он откажется купить слона,
# то мы уберем одну подсказку. Как будто что-то меняется :)
sessionStorage = {}
townmain = {}
tr = None
png = {}
story = {}
main = ''
ugadmain = {}
@app.route('/post', methods=['POST'])
# Функция получает тело запроса и возвращает ответ.
# Внутри функции доступен request.json - это JSON,
# который отправила нам Алиса в запросе POST
def main():
    logging.info(f'Request: {request.json!r}')

    # Начинаем формировать ответ, согласно документации
    # мы собираем словарь, который потом при помощи
    # библиотеки json преобразуем в JSON и отдадим Алисе
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }

    # Отправляем request.json и response в функцию handle_dialog.
    # Она сформирует оставшиеся поля JSON, которые отвечают
    # непосредственно за ведение диалога
    play_town(request.json, response)

    logging.info(f'Response:  {response!r}')

    # Преобразовываем в JSON и возвращаем
    return json.dumps(response)

def play_town(req, res):
    global townmain, png, main, ugadmain, story, sob, sob1, dat, dat1, tr, s, sd
    user_id = req['session']['user_id']
    sessionStorage[user_id] = {
        'suggests': [
            "Игра в города",
            "Угадай город по картинке",
            "Исторические события"
        ],
        'townfirst': ["Наши города будут начинаться на одну и ту же букву",
                      "Начало следующего города, конец предыдущего", "Город можно называть на любую букву"],
        'townsecond': ["Пропустить"],

    }
    if req['session']['new']:
        # Это новый пользователь.
        # Инициализируем сессию и поприветствуем его.
        # Запишем подсказки, которые мы ему покажем в первый раз
        res['response']['text'] = 'Привет! Назови свое имя!'
        # создаем словарь в который в будущем положим имя пользователя
        sessionStorage1[user_id] = {
            'first_name': None,
            "play": None,
            'sit': ""
        }
        story[user_id] = None
        return
    if sessionStorage1[user_id]['first_name'] is None:
        # в последнем его сообщение ищем имя.
        first_name = get_first_name(req)

        # если не нашли, то сообщаем пользователю что не расслышали.
        if first_name is None:
            res['response']['text'] = \
                'Не расслышала имя. Повтори, пожалуйста!'
        # если нашли, то приветствуем пользователя.
        # И спрашиваем какой город он хочет увидеть.
        else:
            sessionStorage1[user_id]['first_name'] = first_name
            res['response'][
                'text'] = 'Приятно познакомиться, ' \
                          + first_name.title() \
                          + '. Я - Алиса. Многофункциональный навык Игры на твоих правилах. Давай объясню правила) ' \
                  'Смешно, правда? Вот именно, никаких правил нет. Выбирай игру, и выбирай, как хочешь играть.'
            # получаем варианты buttons из ключей нашего словаря cities

            townmain[user_id] = False
            ugadmain[user_id] = False
            main = town[random.randint(0, len(town) - 1)]
            townmain[user_id + "2"] = False
            townmain[user_id + "1"] = False
            townmain[user_id + "3"] = False
            res['response']['buttons'] = [
                {
                    'title': v,
                    'hide': True
                } for v in sessionStorage[user_id]["suggests"]
            ]
            return

    # Сюда дойдем только, если пользователь не новый,
    # и разговор с Алисой уже был начат
    # Обрабатываем ответ пользователя.
    # В req['request']['original_utterance'] лежит весь текст,
    # что нам прислал пользователь
    # Если он написал 'ладно', 'куплю', 'покупаю', 'хорошо',
    # то мы считаем, что пользователь согласился.
    # Подумайте, всё ли в этом фрагменте написано "красиво"?
    if req['request']['original_utterance'].lower() in [
        "играем в города",
        "в города",
        "давай в города",
        "игра в города" ]:
        # Пользователь согласился, прощаемся.
        townmain[user_id] = True
        res['response']['text'] = 'Выбирай то, что можно делать в нашей игре'
        res['response']['buttons'] = [
               {
                   'title': v,
                   'hide': True
               } for v in sessionStorage[user_id]["townfirst"]
           ]
        return
    elif req['request']['original_utterance'].lower() == "угадай город по картинке":
        ugadmain[user_id] = True
        res['response']['text'] = 'Отгадаешь город по фото?'
        res['response']['buttons'] = [
            {
                'title': v,
                'hide': True
            } for v in variant
        ]
        return
    elif req['request']['original_utterance'].lower() == "исторические события":
        story[user_id] = True
        res['response']['text'] = 'Сейчас мы проверим насколько хорошо ты занешь историю России) Я буду называть ' \
                                  'даты, а ты должен назвать событие или событие, а ты должен назвать даты) ' \
                                  'Сейчас разберешься)  ПоГНаЛи!!!'

        res['response']['buttons'] = [
            {
                'title': v,
                'hide': True
            } for v in ist
        ]
        return

    if story[user_id]:
        if  "дату" in req['request']['original_utterance'].lower():
            s = sob1[random.randint(0, len(sob1) - 1)]
            tr = True
            res['response']['text'] = f"Когда произошло событие: {s}"
            return
        elif "событие" in req['request']['original_utterance'].lower():
            sd = dat[random.randint(0, len(dat) - 1)]
            tr = False
            name = ''
            name += dat1[sd][0]
            for i in range(1, len(dat1[sd]) - 2):
                if dat1[sd][i] == " ":
                    name += " "
                else:
                    name += "_"
            name += dat1[sd][-1]
            res['response']['text'] = f"Что произошло в: {sd}  \n {name}"
            return
        if tr is True:
            if sob[s] in req['request']['original_utterance'].lower():
                res['response']['text'] = "Правильно. Что будешь отгадывать следующим? Событие или Дату?"
                res['response']['buttons'] = [
                    {
                        'title': v,
                        'hide': True
                    } for v in ist
                ]
                tr = None
                return
            else:
                res['response']['text'] = "Не правильно. Что будешь отгадывать следующим? Событие или Дату?"
                res['response']['buttons'] = [
                    {
                        'title': v,
                        'hide': True
                    } for v in ist
                ]
                tr = None
                return
        elif tr is False:
            if req['request']['original_utterance'].lower() in dat1[sd]:
                res['response']['text'] = "Правильно. Что будешь отгадывать следующим? Событие или Дату?"
                res['response']['buttons'] = [
                    {
                        'title': v,
                        'hide': True
                    } for v in ist
                ]
                tr = None
                return
            else:
                res['response']['text'] = "Не правильно. Что будешь отгадывать следующим? Событие или Дату?"
                res['response']['buttons'] = [
                    {
                        'title': v,
                        'hide': True
                    } for v in ist
                ]
                tr = None
                return
    elif ugadmain[user_id]:
        if sessionStorage1[user_id]['play'] is None:
            if req['request']['original_utterance'].lower() in "нет":
                res['response']['end_session'] = True
                return
            if req['request']['original_utterance'].lower() in "да":
                sessionStorage1[user_id]['play'] = True
                if len(cit) > 0:
                    sit = cit[random.randint(0, len(cit) - 1)]
                    res['response']['card'] = {}
                    res['response']['card']['type'] = 'BigImage'
                    res['response']['card']['title'] = 'Что это за город?'
                    res['response']['card']['image_id'] = cities[sit]
                    sessionStorage1[user_id]['sit'] = sit
                    res['response']['text'] = "Что за город?"
                    return

        if req['request']['original_utterance'].lower() in sessionStorage1[user_id]['sit']:
            res['response']['text'] = "Правильно, сыграем еще?"
            del cit[cit.index(sessionStorage1[user_id]['sit'])]
            sessionStorage1[user_id]['play'] = None
            if len(cit) == 0:
                res['response']['text'] = "Вы угадали все города"
                res['response']['end_session'] = True
            return
        else:
            res['response']['text'] = "Вы пытались. Это 'Название города'. Сыграем еще?"
            sessionStorage1[user_id]['play'] = None
            return
    elif townmain[user_id]:
        if req['request']['original_utterance'].lower() in "наши города будут начинаться на одну и ту же букву":
            townmain[user_id+"1"] = True
            res['response']['text'] = 'Понятно. Вы в любой момент можете спросить, в какой стране расположен город. ' \
                                      'Для этого надо спросить "Какая страна?". Итак, я начну \n' + main
            return
        elif req['request']['original_utterance'].lower() in "начало следующего города, конец предыдущего":
            townmain[user_id + "2"] = True
            res['response']['text'] = 'Понятно. Вы в любой момент можете спросить, в какой стране расположен город. ' \
                                      'Для этого надо спросить "Какая страна?". Итак, я начну \n' + main
            return


        elif req['request']['original_utterance'].lower() in "город можно называть на любую букву":
            townmain[user_id + "3"] = True
            res['response']['text'] = 'Понятно. Вы в любой момент можете спросить, в какой стране расположен город. ' \
                                      'Для этого надо спросить "Какая страна?". Итак, я начну \n' + main
            return

        elif req['request']['original_utterance'].lower() in "какая страна?":
            res['response']['text'] = get_country(main)
        elif req['request']['original_utterance'].lower().title() in town:
            if townmain[user_id + "1"] and main[0].lower() == req['request']['original_utterance'].lower()[0]:
                n = req['request']['original_utterance'].lower().title()
                del town[town.index(n)]
                spis = [w for w in town if w.startswith(n[0].upper())]
                n = spis[random.randint(0, len(spis))]
                main = n
                res['response']['text'] = n
                return
            elif main[0].lower() != req['request']['original_utterance'].lower()[0]:
                res['response']['text'] = f"Увы, но слово не подходит. Оно должно начинаться на букву {main[0]}"

            if townmain[user_id + "2"] and main[-1] == req['request']['original_utterance'].lower()[0]:
                n = req['request']['original_utterance'].lower().title()
                del town[town.index(n)]
                spis = [w for w in town if w.startswith(n[-1].upper())]
                if len(spis) > 0:
                    n = spis[random.randint(0, len(spis))]
                    main = n
                    res['response']['text'] = n
                else:
                    main = town[random.randint(0, len(town))]
                    res['response']['text'] = f"Все города на эту букву закончились, поэтому я назову \n {main}"
            elif main[-1].lower() != req['request']['original_utterance'].lower()[0]:
                res['response']['text'] = f"Увы, но город не подходит. Оно должно начинаться на букву {main[-1]}"

            if townmain[user_id + "3"]:
                n = req['request']['original_utterance'].lower().title()
                del town[town.index(n)]
                n = town[random.randint(0, len(town))]
                res['response']['text'] = n
                del town[town.index(n)]
        elif req['request']['original_utterance'].lower() in "пропустить":
            n = town[random.randint(0, len(town))]
            res['response']['text'] = n
            del town[town.index(n)]
            main = n
            return


        else:
            res['response']['text'] = "Хмм, Не слышала о таком городе в России) Когда воздвигнешь его, вот тогда и " \
                                      "поиграем с ним. Или возможно этот город уже был. Пропустим эту букву?"
            res['response']['buttons'] = res['response']['buttons'] = [
                   {
                       'title': v,
                       'hide': True
                   } for v in sessionStorage[user_id]["townsecond"]
                ]

def get_city(req):
    # перебираем именованные сущности
    for entity in req['request']['nlu']['entities']:
        # если тип YANDEX.GEO то пытаемся получить город(city),
        # если нет, то возвращаем None
        if entity['type'] == 'YANDEX.GEO':
            # возвращаем None, если не нашли сущности с типом YANDEX.GEO
            return entity['value'].get('city', None)


def get_first_name(req):
    # перебираем сущности
    for entity in req['request']['nlu']['entities']:
        # находим сущность с типом 'YANDEX.FIO'
        if entity['type'] == 'YANDEX.FIO':
            # Если есть сущность с ключом 'first_name',
            # то возвращаем ее значение.
            # Во всех остальных случаях возвращаем None.
            return entity['value'].get('first_name', None)

def get_country(city_name):
    try:
        url = "https://geocode-maps.yandex.ru/1.x/"
        params = {
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            'geocode': city_name,
            'format': 'json'
        }
        data = requests.get(url, params).json()
        # все отличие тут, мы получаем имя страны
        return data['response']['GeoObjectCollection'][
            'featureMember'][0]['GeoObject']['metaDataProperty'][
            'GeocoderMetaData']['AddressDetails']['Country']['CountryName']
    except Exception as e:
        return e


def get_suggests(user_id):
    session = sessionStorage[user_id]

    # Выбираем две первые подсказки из массива.
    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests'][:2]
    ]

    # Убираем первую подсказку, чтобы подсказки менялись каждый раз.
    session['suggests'] = session['suggests'][1:]
    sessionStorage[user_id] = session

    # Если осталась только одна подсказка, предлагаем подсказку
    # со ссылкой на Яндекс.Маркет.

    return suggests


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
