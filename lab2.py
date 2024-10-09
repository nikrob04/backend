from flask import Blueprint, url_for, redirect, render_template
lab2 = Blueprint('lab2', __name__)

flower_list = ['роза', 'тюльпан', 'незабудка', 'ромашка']

#для вывода всех цветов и их количества
@lab2.route('/lab2/flowers')
def all_flowers():
    return f'''
<!doctype html>
<html>
    <body>
    <h1>Список всех цветов</h1>
    <p>Количество цветов: {len(flower_list)}</p>
    <ul>
        {''.join(f'<li>{flower}</li>' for flower in flower_list)}
    </ul>
    </body>
</html>
'''

# Улучшенный вывод
@lab2.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list):
        return '''
<!doctype html>
<html>
    <body>
        <h1>Ошибка 404</h1>
        <p>Такого цветка нет</p>
        <a href="/lab2/flowers">Вернуться ко всем цветам</a>
    </body>
</html>
''', 404
    else:
        return f'''
<!doctype html>
<html>
    <body>
    <h1>Цветок: {flower_list[flower_id]}</h1>
    <a href="/lab2/flowers">Вернуться ко всем цветам</a>
    </body>
</html>
'''

# для случая, когда имя цветка не указано
@lab2.route('/lab2/add_flower/')
def add_flower_no_name():
    return '''
<!doctype html>
<html>
    <body>
        <h1>Ошибка 400</h1>
        <p>Вы не задали имя цветка</p>
        <a href="/lab2/flowers">Вернуться ко всем цветам</a>
    </body>
</html>
''', 400

# для добавления нового цветка
@lab2.route('/lab2/add_flower/<name>')
def add_flower(name):
    flower_list.lab2end(name)
    return f'''
<!doctype html>
<html>
    <body>
    <h1>Добавлен новый цветок</h1>
    <p>Название нового цветка: {name}</p>
    <p>Всего цветов: {len(flower_list)}</p>
    <p>Полный список:</p>
    <ul>
        {''.join(f'<li>{flower}</li>' for flower in flower_list)}
    </ul>
    <a href="/lab2/flowers">Вернуться ко всем цветам</a>
    </body>
</html>
'''

# для очистки списка цветов
@lab2.route('/lab2/clear_flowers')
def clear_flowers():
    flower_list.clear()
    return '''
<!doctype html>
<html>
    <body>
    <h1>Список цветов очищен</h1>
    <a href="/lab2/flowers">Вернуться ко всем цветам</a>
    </body>
</html>
'''


@lab2.route('/lab2/example')
def exemple():
    name, lab_num, group, curs = 'Никитенко И.Р.', 2, 'ФБИ-21', 3
    fruits = [{'name': 'яблоки', 'price': 100 },
              {'name': 'груши', 'price': 120},
              {'name': 'апельсины', 'price': 80},
              {'name': 'мандарины','price': 95},
              {'name': 'манго', 'price': 321}
    ]
    return render_template('example.html', name=name, lab_num=lab_num, group=group, curs=curs, fruits=fruits)

@lab2.route('/lab2/')
def lab():
    return render_template('lab2.html')

@lab2.route('/lab2/filters/')
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('filter.html', phrase = phrase)

@lab2.route('/lab2/calc/<int:a>/<int:b>/')
def calc(a, b):
    return f'''
<!doctype html>
<html>
    <body>
    <h1>Мат. операции</h1>
    <p>{a} + {b} = {a+b}</p>
    <p>{a} - {b} = {a-b}</p>
    <p>{a} x {b} = {a*b}</p>
    <p>{a} &divide; {b} = {a/b}</p>
    <p>{a}<sup>{b}</sup> = {a**b}</p>
    
    </body>
</html>
'''
@lab2.route('/lab2/calc/')
def calc_default():
    return redirect('/lab2/calc/1/1')
@lab2.route('/lab2/calc/<int:a>/')
def calc_with_one(a):
    return redirect(f'/lab2/calc/{a}/1')


books = [
    {"author": "Джордж Оруэлл", "title": "1984", "genre": "Антиутопия", "pages": 328},
    {"author": "Рэй Брэдбери", "title": "451 градус по Фаренгейту", "genre": "Антиутопия", "pages": 256},
    {"author": "Михаил Булгаков", "title": "Собачье сердце", "genre": "Фантастика", "pages": 128},
    {"author": "Фёдор Достоевский", "title": "Преступление и наказание", "genre": "Классика", "pages": 672},
    {"author": "Джейсон Шрейер", "title": "Кровь, пот и пиксели", "genre": "Документальная литература", "pages": 320},
    {"author": "Марк Твен", "title": "Приключения Тома Сойера", "genre": "Приключения", "pages": 244},
    {"author": "Дж. Р. Р. Толкин", "title": "Властелин колец", "genre": "Фэнтези", "pages": 1178},
    {"author": "Лев Толстой", "title": "Война и мир", "genre": "Классика", "pages": 1225},
    {"author": "Джейн Остин", "title": "Гордость и предубеждение", "genre": "Роман", "pages": 432},
    {"author": "Харпер Ли", "title": "Убить пересмешника", "genre": "Роман", "pages": 281},
]
@lab2.route('/lab2/books')
def books_list():
    return render_template('books.html', books=books)   


dogs = [
    {"filename": "dogfox.jpg", "name": "Фокстерьер", "description": "Эта собака была предназначена для охоты на лисиц."},
    {"filename": "cwergdog.jpg", "name": "Цвергшнауцер", "description": "Самая маленькая по размеру служебная собака в мире."},
    {"filename": "erdel.jpg", "name": "Эрдельтерьер", "description": "Родина породы — долина реки Эйр в графстве Йоркшир."},
    {"filename": "tibet.jpg", "name": "Тибетский мастиф", "description": "Крупная порода собак, которую исторически разводили в Тибете, Непале, Индии."},
    {"filename": "mops.jpg", "name": "Мопс", "description": "Порода декоративных собак. Мопсы были привезены из Китая в Европу в XVI веке."}
]

@lab2.route('/lab2/dogs')
def show_dogs():
    return render_template('dogs.html', dogs=dogs)