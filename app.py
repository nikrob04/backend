from flask import Flask, url_for, redirect, render_template, session
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
app = Flask (__name__)


app.config['SECRET_KEY'] = os.environ('SECRET_KEY', 'Секретныйключ')
app.config['DB_TYPE'] = os.gatenv('DB_TYPE', 'postgres')

app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)

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
                    <ul>
                        <li><a href="/lab1">Лабораторная 1</a></li>
                        <li><a href="/lab2">Лабораторная 2</a></li>
                        <li><a href="/lab3">Лабораторная 3</a></li>
                        <li><a href="/lab4">Лабораторная 4</a></li>
                        <li><a href="/lab5">Лабораторная 5</a></li>
                    <ul>
                </main>
                <footer>
                    <p>&copy; НГТУ, ФБ, 2024, Никтенко И.Р. Фби-21</p>
                </footer>
            </body>
        </html> '''
@app.route("/index")
def index():
    return redirect("/")


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

