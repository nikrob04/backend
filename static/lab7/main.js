function fillFilmList() {
    fetch('/lab7/rest-api/films')
        .then(function (data) {
            return data.json();
        })
        .then(function (films) {
            let tbody = document.getElementById('film-list');
            tbody.innerHTML = '';
            for (let i = 0; i < films.length; i++) {
                let tr = document.createElement('tr');
                let tdTitleRus = document.createElement('td');
                let tdTitle = document.createElement('td');
                let tdYear = document.createElement('td');
                let tdActions = document.createElement('td');

                // Русское название
                tdTitleRus.innerText = films[i].title_ru;

                // Оригинальное название (курсив и скобки)
                if (films[i].title) {
                    tdTitle.innerHTML = `<em>(${films[i].title})</em>`;
                } else {
                    tdTitle.innerHTML = ''; // Если нет оригинального названия, оставляем пустым
                }

                // Год выпуска
                tdYear.innerText = films[i].year;

                // Кнопки редактирования и удаления
                let editButton = document.createElement('button');
                editButton.innerText = 'редактировать';
                editButton.onclick = function() {
                    editFilm(i);
                }

                let delButton = document.createElement('button');
                delButton.innerText = 'удалить';
                delButton.onclick = function () {
                    deleteFilm(i, films[i].title_ru);
                };

                tdActions.append(editButton);
                tdActions.append(delButton);

                tr.append(tdTitleRus);
                tr.append(tdTitle);
                tr.append(tdYear);
                tr.append(tdActions);

                tbody.append(tr);
            }
        });
}

function deleteFilm(id, title) {
    if (!confirm(`Вы точно хотите удалить фильм "${title}"?`)) return;

    fetch(`/lab7/rest-api/films/${id}`, { method: 'DELETE' })
        .then(function () {
            fillFilmList();
        });
}

function showModal() {
    document.querySelector('div.modal').style.display = 'block';
    document.getElementById('description-error').innerText = '';
}

function hideModal() {
    document.querySelector('div.modal').style.display = 'none';
}

function cancel() {
    hideModal();
}

function addFilm() {
    document.getElementById('id').value = '';
    document.getElementById('title').value = '';
    document.getElementById('title-ru').value = '';
    document.getElementById('year').value = '';
    document.getElementById('description').value = '';
    showModal();
}

function sendFilm() {
    const id = document.getElementById('id').value;
    const film = {
        title: document.getElementById('title').value,
        title_ru: document.getElementById('title-ru').value,
        year: document.getElementById('year').value,
        description: document.getElementById('description').value
    };

    const url = id === '' ? '/lab7/rest-api/films/' : `/lab7/rest-api/films/${id}`;
    const method = id === '' ? 'POST' : 'PUT';

    fetch(url, {
        method: method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(film)
    })
    .then(response => {
        if (response.ok) {
            return response.json(); // Если всё ок, возвращаем JSON
        } else if (response.status === 400) {
            return response.json().then(data => { throw data; }); // Если ошибка 400, выбрасываем данные ошибки
        } else {
            throw { description: 'Произошла ошибка при сохранении данных' };
        }
    })
    .then(data => {
        fillFilmList(); // Успешно обновляем список фильмов
        hideModal();    // Закрываем модальное окно
    })
    .catch(error => {
        if (error.description) {
            document.getElementById('description-error').innerText = error.description; // Отображаем описание ошибки
        } else {
            console.error('Unexpected error:', error);
        }
    });
}

function editFilm(id){
    fetch(`/lab7/rest-api/films/${id}`)
    .then(function (data) {
        return data.json();
    })
    .then(function (film){
        document.getElementById('id').value = id;
        document.getElementById('title').value = film.title;
        document.getElementById('title-ru').value = film.title_ru;
        document.getElementById('year').value = film.year;
        document.getElementById('description').value = film.description;
        showModal();
    })
}

// Запуск функции заполнения списка фильмов при загрузке страницы
document.addEventListener('DOMContentLoaded', fillFilmList);
