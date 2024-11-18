from flask import Blueprint, render_template, request, make_response, redirect, session

lab5 = Blueprint('lab5', __name__)

@lab5.route('/lab5/')
def lab5_index():  # Переименовано, чтобы избежать конфликта
    return render_template('lab5/lab5.html')

@lab5.route('/lab5/login')
def login():
    return "Login Page"  # Добавьте логику

@lab5.route('/lab5/register')
def register():
    return "Register Page"  # Добавьте логику

@lab5.route('/lab5/list')
def list():
    return "List Page"  # Добавьте логику

@lab5.route('/lab5/create')
def create():
    return "Create Page"  # Добавьте логику
