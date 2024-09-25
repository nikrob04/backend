from flask import Flask, url_for, redirect

app = Flask (__name__)

@app.route("/")
@app.route("/web")
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

@app.route("/author")
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
    return '''
    <!doctype html>
    <html>
        <body>
            <h1>Дуб</1>
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
        Сколько раз вы заходили: ''' + str(count) + '''
    </body>
</html>

'''
@app.route("/info")
def info():
    return redirect("/author")

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