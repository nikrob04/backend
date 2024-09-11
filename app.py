from flask import Flask

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
        </html> '''

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