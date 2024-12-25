from flask import Blueprint, render_template, request, session, redirect, url_for, flash, jsonify
import psycopg2
from psycopg2 import extras
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Создаем Blueprint
rgz = Blueprint('rgz', __name__)

# Функция для подключения к базе данных
def db_connect():
    conn = psycopg2.connect(
        host='127.0.0.1',
        database='ilya_rgz',
        user='ilya_rgz',
        password='123'
    )
    return conn

# Главная страница
@rgz.route('/rgz/')
def main():
    conn = db_connect()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    # Получаем первые 5 фильмов
    cur.execute("SELECT id, title, description FROM movies LIMIT 5;")
    movies = cur.fetchall()
    cur.close()
    conn.close()

    # Передаем данные в шаблон
    return render_template('rgz/main.html', movies=movies)

# Список фильмов
@rgz.route('/rgz/movies/')
def movies_list():
    conn = db_connect()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    # Получаем список фильмов
    cur.execute("SELECT id, title, description FROM movies ORDER BY title;")
    movies = cur.fetchall()
    cur.close()
    conn.close()

    # Передаем данные в шаблон
    return render_template('rgz/movies.html', movies=movies)

# Список сеансов
@rgz.route('/rgz/sessions/')
def sessions_list():
    return render_template('rgz/sessions.html')

# Страница регистрации (загружает форму)
@rgz.route('/rgz/register/', methods=['GET'])
def register():
    return render_template('rgz/register.html')

# Страница входа (загружает форму)
@rgz.route('/rgz/login/', methods=['GET'])
def login():
    return render_template('rgz/login.html')

# Выход из системы
@rgz.route('/rgz/logout/')
def logout():
    # Очищаем сессию
    session.clear()
    # Сообщение о выходе
    flash("Вы успешно вышли из системы.", "success")
    # Перенаправляем на главную страницу
    return redirect(url_for('rgz.main'))

# JSON-RPC API
@rgz.route('/rgz/api/', methods=['POST'])
def json_rpc():
    data = request.get_json()
    method = data.get('method')
    params = data.get('params')
    request_id = data.get('id')

    if method == 'get_sessions':
        return handle_get_sessions(params, request_id)
    elif method == 'get_seats':
        return handle_get_seats(params, request_id)
    elif method == 'reserve_seat':
        return handle_reserve_seat(params, request_id)
    elif method == 'cancel_reservation':
        return handle_cancel_reservation(params, request_id)
    elif method == 'add_session':
        return handle_add_session(params, request_id)
    elif method == 'delete_session':
        return handle_delete_session(params, request_id)
    elif method == 'register':
        return handle_register(params, request_id)
    elif method == 'login':
        return handle_login(params, request_id)
    elif method == 'get_movies':
        return handle_get_movies(params, request_id)
    elif method == 'add_movie':
        return handle_add_movie(params, request_id)
    elif method == 'edit_movie':
        return handle_edit_movie(params, request_id)
    elif method == 'delete_movie':
        return handle_delete_movie(params, request_id)
    else:
        return jsonify({
            'jsonrpc': '2.0',
            'id': request_id,
            'error': {'code': -32601, 'message': 'Method not found'}
        }), 404

# Метод добавления фильма
def handle_add_movie(params, request_id):
    if session.get('role') != 'admin':
        return jsonify({
            'jsonrpc': '2.0',
            'id': request_id,
            'error': {'code': -32002, 'message': 'Доступ запрещен'}
        })

    title = params.get('title')
    description = params.get('description')
    duration = params.get('duration')
    release_date = params.get('release_date')

    conn = db_connect()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO movies (title, description, duration, release_date) VALUES (%s, %s, %s, %s)",
        (title, description, duration, release_date)
    )
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({
        'jsonrpc': '2.0',
        'id': request_id,
        'result': {'message': 'Фильм добавлен'}
    })

# Метод редактирования фильма
def handle_edit_movie(params, request_id):
    if session.get('role') != 'admin':
        return jsonify({
            'jsonrpc': '2.0',
            'id': request_id,
            'error': {'code': -32002, 'message': 'Доступ запрещён'}
        })

    movie_id = params.get('id')
    title = params.get('title')
    description = params.get('description')
    duration = params.get('duration')
    release_date = params.get('release_date')

    if not movie_id or not title or not description or not duration or not release_date:
        return jsonify({
            'jsonrpc': '2.0',
            'id': request_id,
            'error': {'code': -32001, 'message': 'Недостаточно данных для редактирования фильма'}
        })

    conn = db_connect()
    cur = conn.cursor()

    try:
        cur.execute("""
            UPDATE movies
            SET title = %s, description = %s, duration = %s, release_date = %s
            WHERE id = %s
        """, (title, description, duration, release_date, movie_id))
        conn.commit()
        return jsonify({
            'jsonrpc': '2.0',
            'id': request_id,
            'result': {'message': 'Фильм успешно отредактирован'}
        })
    except Exception as e:
        conn.rollback()
        return jsonify({
            'jsonrpc': '2.0',
            'id': request_id,
            'error': {'code': -32003, 'message': f'Ошибка сервера: {str(e)}'}
        })
    finally:
        cur.close()
        conn.close()



# Метод получения списка фильмов
def handle_get_movies(params, request_id):
    conn = db_connect()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    # Получаем только те фильмы, которые не удалены
    cur.execute("SELECT id, title, description, duration, release_date FROM movies WHERE is_deleted = FALSE ORDER BY title;")
    movies = cur.fetchall()
    cur.close()
    conn.close()

    # Приводим дату выхода к строковому формату, если она существует
    for movie in movies:
        if movie['release_date']:
            movie['release_date'] = movie['release_date'].strftime('%Y-%m-%d')

    return jsonify({
        'jsonrpc': '2.0',
        'id': request_id,
        'result': {'movies': movies}
    })



# Метод регистрации
def handle_register(params, request_id):
    name = params.get('name')
    login = params.get('login')
    password = params.get('password')
    password_confirm = params.get('password_confirm')

    # Проверяем, совпадают ли пароли
    if password != password_confirm:
        return jsonify({
            'jsonrpc': '2.0',
            'id': request_id,
            'error': {'code': -32000, 'message': 'Пароли не совпадают'}
        })

    # Подключаемся к базе данных
    conn = db_connect()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    # Проверяем, существует ли пользователь с таким логином
    cur.execute("SELECT * FROM users WHERE login = %s", (login,))
    existing_user = cur.fetchone()

    if existing_user:
        cur.close()
        conn.close()
        return jsonify({
            'jsonrpc': '2.0',
            'id': request_id,
            'error': {'code': -32001, 'message': 'Логин уже существует'}
        })

    # Хэшируем пароль
    hashed_password = generate_password_hash(password)

    # Добавляем пользователя
    cur.execute(
        "INSERT INTO users (name, login, password) VALUES (%s, %s, %s)",
        (name, login, hashed_password)
    )
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({
        'jsonrpc': '2.0',
        'id': request_id,
        'result': {'message': 'Регистрация успешна'}
    })



# Метод входа
def handle_login(params, request_id):
    login = params.get('login')
    password = params.get('password')

    conn = db_connect()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    # Проверяем логин
    cur.execute("SELECT * FROM users WHERE login = %s", (login,))
    user = cur.fetchone()

    if not user or not check_password_hash(user['password'], password):
        cur.close()
        conn.close()
        return jsonify({
            'jsonrpc': '2.0',
            'id': request_id,
            'error': {'code': -32000, 'message': 'Неверный логин или пароль'}
        })

    # Успешный вход
    session['user_id'] = user['id']
    session['username'] = user['login']
    session['role'] = user['role']

    cur.close()
    conn.close()

    return jsonify({
        'jsonrpc': '2.0',
        'id': request_id,
        'result': {'message': 'Вход успешен'}
    })

def handle_delete_movie(params, request_id):
    if session.get('role') != 'admin':
        return jsonify({
            'jsonrpc': '2.0',
            'id': request_id,
            'error': {'code': -32002, 'message': 'Доступ запрещен'}
        })

    movie_id = params.get('id')

    try:
        conn = db_connect()
        cur = conn.cursor()

        # Обновляем поле is_deleted
        cur.execute("UPDATE movies SET is_deleted = TRUE WHERE id = %s", (movie_id,))
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({
            'jsonrpc': '2.0',
            'id': request_id,
            'result': {'message': 'Фильм помечен как удалён'}
        })

    except Exception as e:
        return jsonify({
            'jsonrpc': '2.0',
            'id': request_id,
            'error': {'code': -32003, 'message': f'Ошибка сервера: {str(e)}'}
        })

def handle_get_sessions(params, request_id):
    conn = db_connect()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    cur.execute("""
        SELECT s.id, m.title AS movie_title, s.session_time, s.available_seats
        FROM sessions s
        JOIN movies m ON s.movie_id = m.id
        ORDER BY s.session_time;
    """)
    sessions = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify({
        'jsonrpc': '2.0',
        'id': request_id,
        'result': {'sessions': sessions}
    })

# Добавление сеанса
def handle_add_session(params, request_id):
    if session.get('role') != 'admin':
        return jsonify({
            'jsonrpc': '2.0',
            'id': request_id,
            'error': {'code': -32002, 'message': 'Доступ запрещен'}
        })

    movie_id = params.get('movie_id')
    session_time = params.get('session_time')
    available_seats = params.get('available_seats')

    if not movie_id or not session_time or not available_seats:
        return jsonify({
            'jsonrpc': '2.0',
            'id': request_id,
            'error': {'code': -32001, 'message': 'Недостаточно данных для создания сеанса'}
        })

    conn = db_connect()
    cur = conn.cursor()

    try:
        cur.execute("""
            INSERT INTO sessions (movie_id, session_time, available_seats)
            VALUES (%s, %s, %s)
        """, (movie_id, session_time, available_seats))
        conn.commit()
        return jsonify({
            'jsonrpc': '2.0',
            'id': request_id,
            'result': {'message': 'Сеанс успешно добавлен'}
        })
    except Exception as e:
        conn.rollback()
        return jsonify({
            'jsonrpc': '2.0',
            'id': request_id,
            'error': {'code': -32003, 'message': f'Ошибка сервера: {str(e)}'}
        })
    finally:
        cur.close()
        conn.close()

# Удаление сеанса
def handle_delete_session(params, request_id):
    if session.get('role') != 'admin':
        return jsonify({
            'jsonrpc': '2.0',
            'id': request_id,
            'error': {'code': -32002, 'message': 'Доступ запрещен'}
        })

    session_id = params.get('id')

    conn = db_connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM sessions WHERE id = %s", (session_id,))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({
        'jsonrpc': '2.0',
        'id': request_id,
        'result': {'message': 'Сеанс удалён'}
    })

def handle_get_seats(params, request_id):
    session_id = params.get('session_id')

    conn = db_connect()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    
    try:
        # Генерация мест (1-30) с данными о бронировании
        cur.execute("""
            SELECT gs.seat_number AS number, users.login AS user
            FROM generate_series(1, 30) AS gs(seat_number)
            LEFT JOIN reservations
            ON reservations.session_id = %s AND reservations.seat_number = gs.seat_number
            LEFT JOIN users
            ON users.id = reservations.user_id
        """, (session_id,))
        seats = cur.fetchall()

        return jsonify({
            'jsonrpc': '2.0',
            'id': request_id,
            'result': {'seats': seats}
        })

    except Exception as e:
        return jsonify({
            'jsonrpc': '2.0',
            'id': request_id,
            'error': {'code': -32003, 'message': f'Ошибка сервера: {str(e)}'}
        })
    finally:
        cur.close()
        conn.close()



def handle_reserve_seat(params, request_id):
    session_id = params.get('session_id')
    seat_number = params.get('seat_number')
    user_id = session.get('user_id')

    if not user_id:
        return jsonify({
            'jsonrpc': '2.0',
            'id': request_id,
            'error': {'code': -32001, 'message': 'Вы должны быть авторизованы для бронирования места'}
        })

    conn = db_connect()
    cur = conn.cursor()

    try:
        cur.execute("""
            INSERT INTO reservations (session_id, user_id, seat_number)
            VALUES (%s, %s, %s)
        """, (session_id, user_id, seat_number))
        conn.commit()
        return jsonify({
            'jsonrpc': '2.0',
            'id': request_id,
            'result': {'message': 'Место успешно забронировано'}
        })
    except psycopg2.IntegrityError:
        conn.rollback()
        return jsonify({
            'jsonrpc': '2.0',
            'id': request_id,
            'error': {'code': -32002, 'message': 'Место уже занято'}
        })
    except Exception as e:
        conn.rollback()
        return jsonify({
            'jsonrpc': '2.0',
            'id': request_id,
            'error': {'code': -32003, 'message': f'Ошибка сервера: {str(e)}'}
        })
    finally:
        cur.close()
        conn.close()


def handle_cancel_reservation(params, request_id):
    session_id = params.get('session_id')
    seat_number = params.get('seat_number')
    user_id = session.get('user_id')

    conn = db_connect()
    cur = conn.cursor()

    cur.execute("""
        DELETE FROM reservations
        WHERE session_id = %s AND seat_number = %s AND user_id = %s
    """, (session_id, seat_number, user_id))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({
        'jsonrpc': '2.0',
        'id': request_id,
        'result': {'message': 'Бронь успешно снята'}
    })

def handle_edit_session(params, request_id):
    session_id = params.get('id')
    movie_id = params.get('movie_id')
    session_time = params.get('session_time')
    available_seats = params.get('available_seats')

    if not session_id or not movie_id or not session_time or not available_seats:
        return jsonify({
            'jsonrpc': '2.0',
            'id': request_id,
            'error': {'code': -32001, 'message': 'Недостаточно данных для редактирования сеанса'}
        })

    conn = db_connect()
    cur = conn.cursor()

    try:
        cur.execute("""
            UPDATE sessions
            SET movie_id = %s, session_time = %s, available_seats = %s
            WHERE id = %s
        """, (movie_id, session_time, available_seats, session_id))
        conn.commit()
        return jsonify({
            'jsonrpc': '2.0',
            'id': request_id,
            'result': {'message': 'Сеанс успешно отредактирован'}
        })
    except Exception as e:
        conn.rollback()
        return jsonify({
            'jsonrpc': '2.0',
            'id': request_id,
            'error': {'code': -32002, 'message': f'Ошибка редактирования сеанса: {str(e)}'}
        })
    finally:
        cur.close()
        conn.close()

