from flask import Blueprint, render_template, request, session, jsonify, redirect

lab7 = Blueprint('lab7', __name__)

@lab7.route('/lab7/')
def main():
    return render_template('lab7/index.html')

films = [
    {
        "title": "Intouchables",
        "title_ru": "1+1",
        "year": 2011,
        "description": "Пострадав в результате несчастного случая, богатый аристократ Филипп нанимает в помощники человека,\
            который менее всего подходит для этой работы, – молодого жителя предместья Дрисса, только что освободившегося из тюрьмы.\
            Несмотря на то, что Филипп прикован к инвалидному креслу, Дриссу удается привнести в размеренную жизнь аристократа дух приключений."
    },
    {
        "title": "Interstellar",
        "title_ru": "Интерстеллар",
        "year": 2014,
        "description": "Когда засуха, пыльные бури и вымирание растений приводят человечество к продовольственному кризису,\
              коллектив исследователей и учёных отправляется сквозь червоточину (которая предположительно соединяет области пространства-времени через большое расстояние) в путешествие,\
              чтобы превзойти прежние ограничения для космических путешествий человека и найти планету с подходящими для человечества условиями."
    },
    {
        "title": "The Green Mile",
        "title_ru": "Зеленая миля",
        "year": 1999,
        "description": "Пол Эджкомб — начальник блока смертников в тюрьме «Холодная гора»,\
              каждый из узников которого однажды проходит «зеленую милю» по пути к месту казни.\
                  Пол повидал много заключённых и надзирателей за время работы. Однако гигант Джон Коффи,\
                обвинённый в страшном преступлении, стал одним из самых необычных обитателей блока."
    },
    {
        "title": "Fight Club",
        "title_ru": "Бойцовский клуб",
        "year": 1999,
        "description": "Сотрудник страховой компании страдает хронической бессонницей и отчаянно пытается вырваться из мучительно скучной жизни.\
              Однажды в очередной командировке он встречает некоего Тайлера Дёрдена — харизматического торговца мылом с извращенной философией. Тайлер уверен, что самосовершенствование — удел слабых, а единственное, ради чего стоит жить, — саморазрушение.\
            Проходит немного времени, и вот уже новые друзья лупят друг друга почем зря на стоянке перед баром, и очищающий мордобой доставляет им высшее \
                блаженство. Приобщая других мужчин к простым радостям физической жестокости, они основывают тайный Бойцовский клуб,\
                     который начинает пользоваться невероятной популярностью."
    },
    {
        "title": "Shutter Island",
        "title_ru": "Остров проклятых",
        "year": 2009,
        "description": "Два американских судебных пристава отправляются на один из островов в штате Массачусетс,\
              чтобы расследовать исчезновение пациентки клиники для умалишенных преступников.\
                  При проведении расследования им придется столкнуться с паутиной лжи,\
                      обрушившимся ураганом и смертельным бунтом обитателей клиники."
    },
]

@lab7.route('/lab7/rest-api/films/', methods = ['GET'])
def get_films():
    return films

@lab7.route('/lab7/rest-api/films/<int:id>', methods = ['GET'])
def get_film(id):
    if id <= len(films)-1:
        return films[id] 
    else:
        return 'Такого фильма нет', 404
@lab7.route('/lab7/rest-api/films/<int:id>', methods = ['DELETE'])
def del_film(id):
    if id <= len(films)-1:
        del films[id]
        return '', 204
    else:
        return 'Такого фильма нет', 404
    
@lab7.route('/lab7/rest-api/films/<int:id>', methods = ['PUT'])
def put_film(id):
    if id <= len(films)-1:
        film = request.get_json()
        if film['description'] == '':
            return {'description': 'Заполните описаение!'}, 400
        films[id] = film
        return films[id]
    else:
        return 'Такого фильма нет', 404  

@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    film = request.get_json()
    if not film.get('description'):
        return {'description': 'Описание фильма не может быть пустым!'}, 400
    if not film.get('title') and film.get('title_ru'): 
        film['title'] = film['title_ru']  
    films.append(film)
    return jsonify({"id": len(films) - 1}), 201


