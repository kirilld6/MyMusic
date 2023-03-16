<h3>Данное веб-приложение представляет собой онлайн-сервис для прослушивания музыки. Пользователи могут создавать свои
аккаунты, загружать свои песни и просматривать музыкальный контент, который был загружен другими пользователями.</h3>
___
MyMusic.

<h3>Функциональность приложения включает в себя:</h3>
---
1. Регистрацию и авторизацию пользователей.
2. Загрузку песен и информации о них.
4. Возможность прослушивания песен на сайте.
5. Создание плейлиста пользователея и добавление песен в список понравившихся.
6. Просмотр списка понравившихся песен.
7. Управление своими загруженными песнями (удаление).
8. Отображение информации о других пользователях и просмотр их загруженных песен.


### Для создания приложения были использованы следующие технологии:

1. Flask - фреймворк для создания веб-приложений на языке Python.
2. SQLAlchemy - ORM-библиотека для работы с базой данных.
3. Jinja2 - шаблонизатор для формирования веб-страниц.
4. HTML/CSS/JavaScript - языки для создания фронтенда приложения.
5. Bootstrap - фреймворк для создания адаптивных и стильных веб-страниц.
6. SQLite - реляционная база данных, используемая для хранения информации о пользователях и песнях.

<h3>Управление в игре:</h3>
---

1. Для начала игры нажмите пробел
2. Для управления персонажем используйте стрелочки на клавиатуре
3. Во время игры нажмите клавишу ПРОБЕЛА, чтобы начать стрелять

___

<h3>Для корректной сборки проекта необходимо:</h3>
___

### Шаг 1. Установка Python версии 3.9 

Первым шагом необходимо установить Python на компьютер, если его еще нет. Для этого нужно перейти на официальный сайт Python и скачать установщик для Windows. Выберите версию Python 3.x.x и установите на компьютер, следуя инструкциям.

### Шаг 2. Установка зависимостей

Для работы приложения необходимо установить несколько зависимостей. Для этого нужно открыть командную строку и ввести следующую команду:

    pip install -r requirements.txt

### Шаг 3. Создание базы данных

Перед запуском приложения необходимо создать базу данных. Для этого нужно ввести следующие команды в командной строке:

    python
    from app import db
    db.create_all()
    exit()

### Шаг 4. Запуск приложения

Для запуска приложения нужно ввести следующую команду в командной строке:
    
    python run.py

После этого приложение будет доступно по адресу http://localhost:5000.
___

<h3>Структура проекта:</h3>
___

| Название папки | Содержание                                                                                                                                                                                              |
|----------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| app/           | основная папка приложения, содержащая код и ресурсы.                                                                                                                                                    |
| __init__.py    | файл инициализации приложения, где определяются экземпляр Flask и другие настройки приложения.                                                                                                          |
| models.py      | файл, содержащий определения моделей базы данных (таблиц) с помощью SQLAlchemy.                                                                                                                         |
| routes.py      | файл, содержащий определения маршрутов (эндпоинтов) приложения с помощью Flask.                                                                                                                         |
| forms.py       | В директории хранятся иконки в формате png, используемые в приложении                                                                                                                                   |
| instance/      | апка, содержащая конфигурационный файл config.py, который не должен храниться в репозитории, так как содержит секретные данные, такие как ключи для подключения к базе данных и настройки безопасности. |
| templates/:    | папка, содержащая шаблоны HTML для каждой страницы приложения.                                                                                                                                          |
| upload/:       | папка, содержащая загруженные файлы.                                                                                                                                                                    |


<h3>Структура venv:</h3>
___

| Название файла   | Содержание                                  |
|------------------|---------------------------------------------|
| requirements.txt | Файл, с описанием зависимостей и их версии. |
| Constants        | Константы используемые в игре               |
| run.py           | Файл для запуска приложения.                |


### Описание функционала
    Откройте браузер и перейдите по адресу http://localhost:5000/, чтобы открыть главную страницу приложения.

    Для того, чтобы зарегистрироваться в приложении, нажмите на кнопку "Регистрация" и заполните форму.

    После регистрации вы будете автоматически перенаправлены на страницу входа. Введите свой логин и пароль, чтобы войти в систему.

    После входа вы можете добавлять и удалять песни, а также добавлять и удалять их из списка понравившихся.

    Чтобы добавить песню в свой список понравившихся, нажмите на кнопку "Добавить в понравившиеся" на странице песни.

    Чтобы удалить песню из списка понравившихся, нажмите на кнопку "Удалить из понравившихся" на странице песни.

    Чтобы выйти из аккаунта, нажмите на кнопку "Выйти" в правом верхнем углу страницы.



