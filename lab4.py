from flask import Blueprint, render_template, request, make_response, redirect
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
    {'login' : 'alex', 'password': '123'},
    {'login': 'bob', 'password': 'qwerty'},
    {'login': 'rob', 'password': '321'},
    {'login': 'lia', 'password': 'qqq'}
]
@lab4.route('/lab4/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('lab4/login.html', authorized=False)

    login = request.form.get('login')
    password = request.form.get('password')
    
    for user in users:
        if login == user['login'] and password == user['password']:
            return render_template('lab4/login.html', login=login, authorized = True)
    
    error = 'Неверное имя пользователя или пароль'
