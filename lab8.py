from flask import Blueprint, render_template, request, session, jsonify, redirect
from db import db
from db.models import users, articles
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, login_required, current_user, logout_user


lab8 = Blueprint('lab8', __name__)


@lab8.route('/lab8/')
def lab8_index():
    if current_user.is_authenticated:
        username = current_user.login  # Логин пользователя
    else:
        username = "Аноним"  # Если пользователь не авторизован
    return render_template('lab8/index.html', username=username)

@lab8.route('/lab8/login/', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab8/login.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')
    if request.form.get('remember'):
        remember_me = True 
    else:
        remember_me = False

    user = users.query.filter_by(login =  login_form).first()

    if not login_form or not password_form:
        return render_template('lab8/login.html',
                               error = 'Веведите логин/пароль')

    if user:
        if check_password_hash(user.password, password_form):
            login_user(user, remember = remember_me)
            return redirect ('/lab8/')
    
    return render_template ('lab8/login.html', error = 'Ошибка входа: неверный(ые) логин/пароль')
    

@lab8.route('/lab8/register/', methods = ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')
    
    login_exists = users.query.filter_by(login =  login_form).first()
    
    if not login_form or not password_form:
        return render_template('lab8/register.html',
                               error = 'Веведите логин/пароль')

    if login_exists:
        return render_template('lab8/register.html',
                               error = 'Такой пользователь уже существует')
    
    
    password_hash = generate_password_hash(password_form)
    new_user = users(login = login_form, password = password_hash)
    db.session.add(new_user)
    db.session.commit()
    login_user(new_user, remember = False)
    return redirect ('/lab8/')
    

@lab8.route('/lab8/articles/', methods=['GET'])
@login_required
def articles_list():
    user_articles = articles.query.filter_by(login_id=current_user.id).all()
    return render_template('lab8/articles.html', articles=user_articles)

@lab8.route('/lab8/create', methods=['GET', 'POST'])
@login_required  # Доступ только для авторизованных пользователей
def create_article():
    if request.method == 'GET':
        return render_template('lab8/create.html')  # Форма создания статьи

    # Получаем данные из формы
    title_form = request.form.get('title')
    article_text_form = request.form.get('article_text')

    # Проверяем на пустые значения
    if not title_form or not article_text_form:
        return render_template('lab8/create.html',
                               error='Введите название и текст статьи')

    # Создаем новую статью
    new_article = articles(
        title=title_form,
        article_text=article_text_form,
        login_id=current_user.id  # Привязываем статью к текущему пользователю
    )

    # Добавляем и сохраняем в базе данных
    db.session.add(new_article)
    db.session.commit()

    # Перенаправляем на страницу со статьями
    return redirect('/lab8/articles')

@lab8.route('/lab8/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect('/lab8/')

@lab8.route('/lab8/edit/<int:article_id>', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    # Получаем статью по ID
    article = articles.query.get_or_404(article_id)

    # Проверяем, что статья принадлежит текущему пользователю
    if article.login_id != current_user.id:
        return render_template('lab8/articles.html', error='У вас нет прав на редактирование этой статьи.')

    if request.method == 'POST':
        # Обновляем данные статьи
        title_form = request.form.get('title')
        article_text_form = request.form.get('article_text')

        if not title_form or not article_text_form:
            error = 'Название и текст статьи обязательны!'
            return render_template('lab8/edit.html', article=article, error=error)

        article.title = title_form
        article.article_text = article_text_form

        db.session.commit()
        return redirect('/lab8/articles')

    return render_template('lab8/edit.html', article=article)

@lab8.route('/lab8/delete/<int:article_id>', methods=['POST'])
@login_required
def delete_article(article_id):
    # Получаем статью по ID
    article = articles.query.get_or_404(article_id)

    # Проверяем, что статья принадлежит текущему пользователю
    if article.login_id != current_user.id:
        return render_template('lab8/articles.html', error='У вас нет прав на удаление этой статьи.')

    # Удаляем статью
    db.session.delete(article)
    db.session.commit()

    return redirect('/lab8/articles')
