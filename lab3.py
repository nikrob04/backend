from flask import Blueprint, url_for, redirect, render_template, request, make_response
lab3 = Blueprint('lab3', __name__)

@lab3.route('/lab3/')
def lab():
    name = request.cookies.get('name')
    name_color = request.cookies.get('name_color')
    return render_template('lab3/lab3.html', name=name, name_color=name_color) 

@lab3.route('/lab3/cookie/')
def cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name', 'Alex', max_age=5)
    resp.set_cookie('age', '20')
    resp.set_cookie('name_color', 'magenta')
    return resp

@lab3.route('/lab3/del_cookie/')
def del_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')
    return resp

@lab3.route('/lab3/form1')
def form1():
    errors = {}
    user =  request.args.get('user')
    if user == '':
        errors['user'] = 'Заполните поле!'
    age = request.args.get('age')
    if age == '':
        errors['age'] = 'Заполните возраст!'
    sex = request.args.get('sex')
    return render_template('lab3/form1.html', user=user, age=age, sex=sex, errors=errors)

@lab3.route('/lab3/order')
def order():
    return render_template('/lab3/order.html')

@lab3.route('/lab3/pay')
def pay():
    price = 0
    drink = request.args.get('drink')
    if drink == 'cofee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 70

    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on':
        price += 10
    return render_template('lab3/pay.html', price=price)

@lab3.route('/lab3/success')
def success(): 
    price = request.args.get('price', 0)
    return render_template('lab3/success.html', price=price)

@lab3.route('/lab3/settings')
def settings():
    color = request.args.get('color')
    fontsize = request.args.get('font-size')
    backgroundcolor = request.args.get('background-color')
    fontfamily = request.args.get('font-family')
    
    if color or fontsize or backgroundcolor or fontfamily:
        resp = make_response(redirect('/lab3/settings'))
        if color:
            resp.set_cookie('color', color)
        if fontsize:
            resp.set_cookie('font-size', f"{fontsize}px")
        if backgroundcolor:
            resp.set_cookie('background-color', backgroundcolor)
        if fontfamily:
            resp.set_cookie('font-family', fontfamily)
        return resp
    
    fontfamily = request.cookies.get('font-family')
    fontsize = request.cookies.get('font-size')
    color = request.cookies.get('color')
    backgroundcolor = request.cookies.get('background-color')
    
    resp = make_response(render_template('lab3/settings.html', color=color, fontsize=fontsize, backgroundcolor=backgroundcolor, fontfamily=fontfamily))
    return resp

@lab3.route('/lab3/railway', methods=['GET', 'POST'])
def railway():
    errors = {}
    user = ''
    age = ''
    sex = ''
    place = ''
    departure = ''
    arrival = ''
    date = ''
    insurance = False

    if request.method == 'POST':
        user = request.form.get('user')
        age = request.form.get('age')
        sex = request.form.get('sex')
        place = request.form.get('place')
        departure = request.form.get('departure')
        arrival = request.form.get('arrival')
        date = request.form.get('date')
        insurance = request.form.get('insurance')

        # Проверка всех полей
        if not user:
            errors['user'] = 'Заполните поле!'
        
        if not age or not age.isdigit() or not (1 <= int(age) <= 120):
            errors['age'] = 'Введите корректный возраст от 1 до 120 лет!'
        
        if not departure:
            errors['departure'] = 'Заполните пункт отправления!'
        
        if not arrival:
            errors['arrival'] = 'Заполните пункт прибытия!'
        
        if not date:
            errors['date'] = 'Выберите дату!'

        if not errors:
            # Если ошибок нет, перенаправляем на страницу с оплатой
            return redirect(url_for('lab3.payrail', user=user, age=age, sex=sex, place=place, 
                                    departure=departure, arrival=arrival, date=date, 
                                    insurance='on' if insurance else 'off'))

    # Отображаем форму с ошибками (если есть) или просто GET запрос
    return render_template(
        'lab3/railway.html', 
        user=user, age=age, sex=sex, place=place,
        departure=departure, arrival=arrival, date=date, 
        errors=errors
    )


@lab3.route('/lab3/payrail')
def payrail():
    user = request.args.get('user')
    age = int(request.args.get('age'))
    place = request.args.get('place')
    insurance = request.args.get('insurance') == 'on'

    # Расчет стоимости
    price = 1000 if age >= 18 else 700

    # Доплата за полку (нижняя или нижняя боковая)
    if place in ['leftdawn', 'rightdawn']:
        price += 100

    # Доплата за страховку
    if insurance:
        price += 150

    # Определяем тип билета
    ticket_type = 'Взрослый билет' if age >= 18 else 'Детский билет'

    return render_template('lab3/payrail.html', user=user, ticket_type=ticket_type, price=price)

@lab3.route('/lab3/clear_settings')
def clear_settings():

    resp = make_response(redirect(url_for('lab3.settings')))
    
    resp.delete_cookie('color')
    resp.delete_cookie('font-size')
    resp.delete_cookie('background-color')
    resp.delete_cookie('font-family')
    
    return resp

