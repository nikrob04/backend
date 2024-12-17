from flask import Blueprint, render_template, request, session, redirect, url_for

lab9 = Blueprint('lab9', __name__)

@lab9.route('/lab9/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':  # Если запрос POST
        name = request.form.get('name')
        if not name or name == '':  # Если имя пустое, возвращаем ошибку
            return render_template('lab9/index.html', error="Введите имя!")
        session['name'] = name  # Сохраняем имя в сессии
        return redirect('/lab9/step2')  # Переходим ко второму шагу
    return render_template('lab9/index.html')  # Если GET, просто отображаем форму


@lab9.route('/lab9/step2/', methods=['GET', 'POST'])
def step2():
    if request.method == 'GET':
        return render_template('lab9/step2.html')  # Проверяем только при POST-запросе
    age = request.form.get('age')  # Получаем возраст из формы
    
        # Проверка на пустое значение (если поле не заполнено)
    if not age or age == '':
            return render_template('lab9/step2.html', error="Введите возраст!")

    age = int(age)  # Преобразуем возраст в целое число

    # Проверка на допустимый возраст (от 1 до 140)
    if age < 1 or age > 140:
        return render_template('lab9/step2.html', error="Возраст должен быть от 1 до 140 лет!")

    session['age'] = age  # Сохраняем возраст в сессии
    return redirect(url_for('lab9.step3'))  # Переходим к следующему шагу

    # При GET-запросе просто отображаем форму
    



@lab9.route('/lab9/step3/', methods=['GET', 'POST'])
def step3():
    if request.method == 'POST':  # Если запрос POST
        sex = request.form.get('sex')  # Получаем выбранный пол

        if not sex:  # Если пол не выбран
            return render_template('lab9/step3.html', error="Пожалуйста, выберите пол!")

        session['sex'] = sex  # Сохраняем выбранный пол в сессии
        return redirect('/lab9/step4/')
    
    return render_template('lab9/step3.html')  # Если GET, просто отображаем форму

@lab9.route('/lab9/step4/', methods=['GET', 'POST'])
def step4():
    if request.method == 'GET':
        return render_template('lab9/step4.html')  # Если запрос POST
    preference = request.form.get('preference')  # Получаем предпочтение пользователя

    if not preference:  # Если предпочтение не выбрано
        return render_template('lab9/step4.html', error="Пожалуйста, выберите вариант!")

    session['preference'] = preference  # Сохраняем предпочтение в сессии
    return redirect('/lab9/step5/')



# Шаг 5: Обработка выбора, зависит от предпочтения пользователя
@lab9.route('/lab9/step5/', methods=['GET', 'POST'])
def step5():
    preference = session.get('preference')  # Получаем предпочтение из сессии  # Если предпочтение не установлено, перенаправляем на step4

    # Если предпочтение - "Что-то вкусное"
    if preference == 'tasty':
        options = [
            ('tasty_caloric', 'Я люблю что-то калорийное'),
            ('tasty_juicy', 'Я люблю что-то сочное')
        ]
    # Если предпочтение - "Что-то красивое"
    elif preference == 'beautiful':
        options = [
            ('beautiful_scented', 'Я люблю приятно пахнущее'),
            ('beautiful_practical', 'Я люблю практичное')
        ]
    else:
        return redirect(url_for('lab9.step4'))  # Если предпочтение не установлено, перенаправляем на step4

    if request.method == 'POST':  # Если запрос POST
        choice = request.form.get('choice')  # Получаем выбранный вариант

        if not choice:  # Если не выбран вариант
            return render_template('lab9/step5.html', options=options, error="Пожалуйста, выберите вариант!")

        session['choice'] = choice  # Сохраняем выбор в сессии
        return redirect('/lab9/step6/')


    return render_template('lab9/step5.html', options=options)  # Отображаем форму с выбором

@lab9.route('/lab9/step6/')
def step6():
    # Получаем данные из сессии
    name = session.get('name')
    sex = session.get('sex')
    preference = session.get('preference')
    choice = session.get('choice')



    # Логика поздравления в зависимости от пола
    if sex == 'male':
        greeting = f"Привет, {name}! Поздравляю тебя с Новым Годом! Ты был хорошим парнем в этом году."
    else:
        greeting = f"Привет, {name}! Поздравляю тебя с Новым Годом! Ты была хорошей девочкой в этом году."

    # Логика подарка в зависимости от предпочтений
    if preference == 'tasty':
        if choice == 'tasty_caloric':
            gift = 'Тазик оливье'
            image = 'https://avatars.dzeninfra.ru/get-zen_doc/1712263/pub_5dfa080ad7859b00b2dd12c6_5dfa09a38f011100ad77ce27/scale_1200'  # Пример URL изображения
        elif choice == 'tasty_juicy':
            gift = 'Ведро мандаринов'
            image = 'https://images.freeimages.com/images/premium/previews/2265/22658725-bucket-full-of-fresh-tangerines.jpg'  # Пример URL изображения
    elif preference == 'beautiful':
        if choice == 'beautiful_scented':
            gift = 'Новогодняя натуральная елка'
            image = 'https://www.sadovod.org/upload/resize_cache/iblock/26d/412_550_14a362258002b3dca428a5b2307d3f3d5/26d0efe080195b58316d36ddfaa2d5ae.jpg'  # Пример URL изображения
        elif choice == 'beautiful_practical':
            gift = 'Искусственная елка'
            image = 'https://www.elkaekb.ru/images/product/l/1740a9ff.jpg'  # Пример URL изображения

    return render_template('lab9/step6.html', greeting=greeting, gift=gift, image=image)