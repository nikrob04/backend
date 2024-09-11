from flask import Flask

app = Flask (__name__)

@app.route("/")
def strt():
    return "web-сервер на flask"