from flask import Flask, url_for, redirect

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
                    <h1>Лабораторная 1</h1>
                </header>
                <main>
                    <p>Flask — фреймворк для создания веб-приложений на языке программирования Python, 
                    использующий набор инструментов Werkzeug, а также шаблонизатор Jinja2. Относится к категории так называемых микрофреймворков —
                    минималистичных каркасов веб-приложений, сознательно предоставляющих лишь самые базовые возможности.</p>
                    <p><a href="/">Вернуться на главную страницу</a></p>

                    <h2>Ссылки задания</h2>
                    <ul>
                        <li><a href="/lab1/oak">Дуб</a></li>
                        <li><a href="/lab1/counter">Счётчик посещений</a></li>
                        <li><a href="/lab1/created">Создание</a></li>
                    </ul>
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
    return "Страница не найдена", 404

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


