from flask import Blueprint, url_for, redirect
lab1 = Blueprint('lab1', __name__)

@lab1.route("/lab1")
def lab():
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


@lab1.route("/lab1/web")
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


@lab1.route("/lab1/author")
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


@lab1.route('/lab1/oak')
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

@lab1.route('/lab1/counter')
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


@lab1.route('/lab1/re_counter')
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


@lab1.route("/lab1/info")
def info():
    return redirect("/lab1/author")


@lab1.route("/lab1/created")
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


@lab1.route("/lab1/onemore")
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
