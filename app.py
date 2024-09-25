from flask import Flask, url_for, redirect, render_template

app = Flask (__name__)

@app.route("/")
def zero():
    return '''
    <!doctype html> 
        <html>
            <head>
                <title>НГТУ, ФБ, Лабораторные работы</title> 
                <style>
                        
                        body {
                            font-family: Arial, sans-serif;
                            margin: 0;
                            padding: 0;
                            background-color: #f0f0f0;
                        }
                        header {
                            background-color: #225a8b;
                            color: white;
                            padding: 20px;
                            text-align: center;
                        }
                        footer {
                            background-color: #225a8b;
                            color: white;
                            padding: 10px;
                            text-align: center;
                            position: absolute;
                            width: 100%;
                            bottom: 0;
                        }
                        main {
                            padding: 20px;
                            text-align: center;
                        }
                </style>
            </head>
            <body>
                <header>
                    <h1>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных</h1>
                </header>
                <main>
                    <h2>Список лабораторных работ</h2>
                    <a href="/lab1">Лабораторная 1</a></li>
                </main>
                <footer>
                    <p>&copy; НГТУ, ФБ, 2024, Никтенко И.Р. Фби-21</p>
                </footer>
            </body>
        </html> '''
@app.route("/index")
def index():
    return redirect("/")


@app.route("/lab1")
def lab1():
    return '''
    <!doctype html> 
        <html>
            <head>
                <title>Лабораторная 1</title> 
                <style>
                    body {
                            font-family: Arial, sans-serif;
                            margin: 0;
                            padding: 0;
                            background-color: #f0f0f0;
                        }
                        header {
                            background-color: #225a8b;
                            color: white;
                            padding: 20px;
                            text-align: center;
                        }
                        footer {
                            background-color: #225a8b;
                            color: white;
               
                            text-align: center;
                            position: absolute;
                            width: 100%;
                            bottom: 0;
                        }
                        main {
                  
                            text-align: center;
                        }
                </style>
            </head>
            <body>
                <header>
                    <h1>Лабораторная 1</h1>
                </header>
                <main>
                    <p>Flask — фреймворк для создания веб-приложений на языке программирования Python, 
                    использующий набор инструментов Werkzeug, а также шаблонизатор Jinja2. Относится к категории так называемых микрофреймворков —
                    минималистичных каркасов веб-приложений, сознательно предоставляющих лишь самые базовые возможности.</p>
                    <h2>Ссылки задания</h2>
                    <ul>
                        <li><a href="/lab1/oak">Дуб</a></li>
                        <li><a href="/lab1/counter">Счётчик посещений</a></li>
                        <li><a href="/lab1/created">Создание</a></li>
                        <li><a href="/lab1/cause_error">500 Ошибка</a></li>
                        <li><a href="/lab1/web">Web</a></li>
                        <li><a href="/lab1/author">Автор</a></li>
                        <li><a href="/lab1/onemore">Best car</a></li>
                        <li><a href="/error/400">400</a></li>
                        <li><a href="/error/401">401</a></li>
                        <li><a href="/error/402">402</a></li>
                        <li><a href="/error/403">403</a></li>
                        <li><a href="/error/418">418</a></li>
                    </ul>
                    <p><a href="/">Вернуться на главную страницу</a></p>
                </main>
                <footer>
                    <p>&copy; НГТУ, ФБ, 2024, Никтенко И.Р. Фби-21</p>
                </footer>
            </body>
        </html>
    '''



@app.route("/lab1/web")
def start():
    return '''<!doctype html> 
        <html>
           <body>
               <h1>web-сервер на flask</h1> 
               <a href="/author">author</a>
           </body>
        </html> ''', 200, {
            'X-server': 'sample',
            'Content-type': 'text/plain; charset=utf-8'
            }

@app.route("/lab1/author")
def author():
    name = "Никитенко Илья Рманович"
    group = "ФБИ-21"
    faculty = "ФБ"

    return '''<!doctype html>
            <html>
                <body>
                    <p>Студент: ''' + name + '''</p>
                    <p>Группа: ''' + group + '''</p>
                    <p>Факультет ''' + faculty + '''</p>
                    <a href="/web">web</a>
                </body>
            </html>'''


@app.route('/lab1/oak')
def oak():
    path = url_for("static", filename="oak.jpg")
    css_path = url_for("static", filename="lab1.css")
    return '''
    <!doctype html>
    <html>
        <head>
            <link rel="stylesheet" type="text/css" href="''' + css_path + '''">
        </head>
        <body>
            <h1>Дуб</h1>
            <img src="''' + path + '''">
        </body>
    </html>
    '''

count = 0

@app.route('/lab1/counter')
def counter():
    global count
    count += 1
    return '''
<!doctype html>
<html>
    <body>
        Сколько раз вы заходили: ''' + str(count) + '''<br>
        <a href="/lab1/re_counter">Сбросить счётчик</a>
    </body>
</html>
'''

@app.route('/lab1/re_counter')
def reset_counter():
    global count
    count = 0 
    return '''
<!doctype html>
<html>
    <body>
        <h1>Счётчик сброшен</h1>
        <a href="/lab1/counter">Вернуться на страницу счётчика</a>
    </body>
</html>
'''


@app.route("/lab1/info")
def info():
    return redirect("/lab1/author")

@app.route("/lab1/created")
def created():
    return '''
<!doctype html>
<html>
    <body>
        <h1>Созданно успешно</h1>
        <div>Что-то там</div>
    </body>
</html>
''', 201

@app.errorhandler(404)
def not_found(err):
    path = url_for("static", filename="cat.jpg")
    return '''
<!doctype html>
<html>
    <head>
        <style>
        img {
            border: 5px solid #228B22;
            border-radius: 10px;
            max-width: 100%;
            height: auto;
        }
        body {
            font-family: Arial, sans-serif;
            background-color: #FFDAB9;
        }
        </style>
        
    </head>
    <body>
        <h1>Ты думал что-то здесь будет?</h1>
        <div>Здесь никогда ничего небыло и, наверное, не будет, поищи в другом месте</div>
        <img src="''' + path + '''">
    </body>
</html>
''', 404

@app.route("/error/400")
def error_400():
    return "Ошибка 400: Неверный запрос", 400

@app.route("/error/401")
def error_401():
    return "Ошибка 401: Требуется авторизация", 401

@app.route("/error/402")
def error_402():
    return "Ошибка 402: Требуется оплата", 402

@app.route("/error/403")
def error_403():
    return "Ошибка 403: Доступ запрещён", 403

@app.route("/error/405")
def error_405():
    return "Ошибка 405: Метод не поддерживается", 405

@app.route("/error/418")
def error_418():
    return "Ошибка 418: Я - чайник ( Эта ошибка ссылается на Hyper Text Coffee Pot Control Protocol (гипертекстовый протокол кофейников) который был первоапрельской шуткой в 1998 году.)", 418

@app.route("/lab1/cause_error")
def cause_error():
    return 1 / 0

@app.errorhandler(500)
def internal_server_error(e):
    return '''
    <!doctype html>
    <html>
        <head>
            <title>Ошибка 500 - Внутренняя ошибка сервера</title>
        </head>
        <body>
            <h1>Внутренняя ошибка сервера (500)</h1>
            <p>Произошла ошибка на сервере. Пожалуйста, попробуйте снова позже.</p>
            <a href="/">Вернуться на главную страницу</a>
        </body>
    </html>
''', 500

@app.route("/lab1/onemore")
def onemore():
    img_paht = url_for('static', filename='car.jpg')
    return '''
    <!doctype html>
    <html>
        <head>
            <title>Очень надежная машина</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 20px;
                    background-color: #f0f0f0;
                }
                h1 {
                    color: #225a8b;
                }
                p {
                    font-size: 18px;
                    color: #333;
                }
                img {
                    width: 100%;
                    max-width: 600px;
                    height: auto;
                    border: 1px solid #ccc;
                    border-radius: 10px;
                    margin-top: 20px;
                }
            </style>
        </head>
        <body>
            <h1>Мой крайне наджный автомобиль</h1>
            <p> Автомобиль назван в честь племени кашкаев (существует также вариант прочтения «кашк'и») из иранской провинции Фарс. Первое поколение было известно как Nissan Dualis в Японии и Австралии и как Nissan Xiaoke в Китае.</p>
            <p>Вот пример изображения, которое я выбрал для оформления страницы:</p>
            <img src="''' + img_paht + '''">
        </body>
    ''', 200, {
        'Content-Language': 'ru',
        'Developer': 'Nikitenko',
        'Powered-By': 'Py',
    }

#Laba2

flower_list = ['роза', 'тюлпан', 'незабудка', 'ромашка']
@app.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list):
        return "Такого цветка нет", 404
    else:
        return "цветок: " + flower_list[flower_id]

@app.route('/lab2/add_flower/<name>')
def add_flower(name):
    flower_list.append(name)
    return f'''
<!doctype html>
<html>
    <body>
    <h1>Добавлен новый цветок</h1>
    <p>Название нового цветка:  {name} </p>
    <p>Всего цветов: {len(flower_list)}</p>
    <p>Полный список: {flower_list}</p>
    </body>
</html>
'''

@app.route('/lab2/example')
def exemple():
    return render_template('example.html')
