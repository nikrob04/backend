from flask import Blueprint, render_template, request, make_response, redirect, session
lab4 = Blueprint('lab4', __name__)

@lab4.route('/lab4/')
def lab():
    return render_template('lab4/lab4.html')

@lab4.route('/lab4/div-form')
def div_form():
    return render_template('lab4/div-form.html')

@lab4.route('/lab4/div', methods=['POST'])
def div():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
  
    if x1 == '' or x2 == '':
        return render_template('lab4/div.html', error='Оба поля должны быть заполнены!')
    
    else:
        x1 = int(x1)
        x2 = int(x2)
        if x2 == 0:
            return render_template('lab4/div.html', error='Деление на ноль невозможно!')
        
        result = x1 / x2
        return render_template('lab4/div.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/sum-form')
def sum_form():
    return render_template('lab4/sum-form.html')

@lab4.route('/lab4/sum', methods=['POST'])
def summ():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    if x1 == '':
        x1 = 0
    if x2 == '':
        x2 = 0

    x1 = int(x1)
    x2 = int(x2)
    result = x1 + x2  
    return render_template('lab4/sum.html', x1=x1, x2=x2, result=result)
        
@lab4.route('/lab4/multi-form')
def multi_form():
    return render_template('lab4/multi-form.html')

@lab4.route('/lab4/multi', methods=['POST'])
def multi():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    if x1 == '':
        x1 = 1
    if x2 == '':
        x2 = 1

    x1 = int(x1)
    x2 = int(x2)
    result = x1 * x2
    return render_template('lab4/multi.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/sub-form')
def sub_form():
    return render_template('lab4/sub-form.html')

@lab4.route('/lab4/sub', methods=['POST'])
def sub():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    if x1 == '' or x2 == '':
        return render_template('lab4/sub.html', error='Оба поля должны быть заполнены!')
    
    else:
        x1 = int(x1)
        x2 = int(x2)

    x1 = int(x1)
    x2 = int(x2)
    result = x1 - x2
    return render_template('lab4/sub.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/power-form')
def power_form():
    return render_template('lab4/power-form.html')

@lab4.route('/lab4/power', methods=['POST'])
def power():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    if x1 == '' or x2 == '':
        return render_template('lab4/power.html', error='Оба поля должны быть заполнены!')
    if x1 == '0' and x2 == '0':
        return render_template('lab4/power.html', error='Оба числа не должны быть равны нулю!')
    else:
        x1 = int(x1)
        x2 = int(x2)

    x1 = int(x1)
    x2 = int(x2)
    result = x1 ** x2
    return render_template('lab4/power.html', x1=x1, x2=x2, result=result)

tree_count = 0

@lab4.route('/lab4/tree', methods = ['POST', 'GET'])
def tree():
    global tree_count
    

    operation = request.form.get('operation')

    if operation == 'cut':
        tree_count -= 1
    elif operation == 'plant':
        tree_count += 1

    if request.method == 'GET':
        return render_template('lab4/tree.html', tree_count=tree_count)
    return redirect('/lab4/tree')


users = [
    {'login' : 'alex', 'password': '123', 'name' : 'Алексей Алексеевич'},
    {'login': 'bob', 'password': 'qwerty', 'name' : 'Никита Романенко'},
    {'login': 'rob', 'password': '321', 'name' : 'Роб Старк'},
    {'login': 'lia', 'password': 'qqq', 'name' : 'Илья Мэдисон'}
]
@lab4.route('/lab4/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'GET':
        if 'login' in session:
            authorized = True
            login = session['login']
            name = session.get('name', '')
        else:
            authorized = False
            login =''
            name = ''
        return render_template('lab4/login.html', authorized=authorized, login = login, name = name)

    login = request.form.get('login')
    password = request.form.get('password')
    
    if login == '' or password == '':
        error = 'Поля должны быть заполнены'
        return render_template('lab4/login.html', login=login, authorized = False, error = error)

    for user in users:
        if login == user['login'] and password == user['password']:
            session['login'] = login
            session['name'] = user['name']
            return redirect('/lab4/login')
            
    
    error = 'Неверное имя пользователя или пароль'
    return render_template('lab4/login.html', login=login, authorized = False, error = error)

@lab4.route('/lab4/logout', methods = ['POST'])
def logout():
    session.pop('login', None)
    return redirect('/lab4/login')


@lab4.route('/lab4/frige', methods=['POST', 'GET'])
def frige():
    if request.method == 'GET':
        return render_template('lab4/frige.html')

    temperature = request.form.get('temperature')

    if temperature == '':
        error = 'Введите температуру'
        return render_template('lab4/frige.html', error=error)

    temperature = int(temperature)
    

    if temperature >= -1:
        error = 'Не удалось установить температуру — слишком высокое значение'
        return render_template('lab4/frige.html', temperature=-2, error=error)
    elif temperature <= -12:
        error = 'Не удалось установить температуру — слишком низкое значение'
        return render_template('lab4/frige.html', temperature=-11, error=error)

    snowflakes_count = 0
    if -12 <= temperature <= -9:
        message = f"Установлена температура: {temperature}°С"
        snowflakes_count = 3  # три снежинки
    elif -8 <= temperature <= -5:
        message = f"Установлена температура: {temperature}°С"
        snowflakes_count = 2  # две снежинки
    elif -4 <= temperature <= -1:
        message = f"Установлена температура: {temperature}°С"
        snowflakes_count = 1  # одна снежинка
    else:
        message = f"Установлена температура: {temperature}°С"

    return render_template('lab4/frige.html', temperature=temperature, message=message, snowflakes_count=snowflakes_count)


@lab4.route('/lab4/order-grain', methods = ['POST', 'GET'])
def order_grain():
    if request.method == 'GET':
        return render_template('lab4/order-grain.html', ordered=False)
    
    grain = request.form.get('grain')
    count = request.form.get('count')
    if grain == '' or count == '':
        error = 'Введите данные'
        return render_template('lab4/order-grain.html', error=error, ordered=False)
    
    count = int(count)

    if count > 500:
        error = 'Такого объема сейчас нет в наличии'
        return render_template('lab4/order-grain.html', error=error, ordered=False)
    if count <= 0:
        error = 'Введите правильный вес'
        return render_template('lab4/order-grain.html', error=error, ordered=False)
    
    grain_names = {
        'barley': 'Ячмень',
        'oat': 'Овес',
        'wheat': 'Пшеница',
        'rye': 'Рожь'
    }

    if grain == 'barley':
        price = 12345
    elif grain == 'oat':
        price = 8522
    elif grain == 'wheat':
        price = 8722
    elif grain == 'rye':
        price = 14111

    if count > 50:
        dis = (price*count)*0.10
        con = price*count-dis
    else:
        dis = 0
        con = price*count

    return render_template ('lab4/order-grain.html', con = con, dis= dis, ordered=True, count=count, grain=grain_names.get(grain, grain))


    

    