# Импортируем необходимые модули
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_uploads import UploadSet, configure_uploads, AUDIO
from instance.config import SECRET_KEY, SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS

app = Flask(__name__, template_folder='../templates')  # создание объекта Flask
app.config['SECRET_KEY'] = SECRET_KEY  # установка секретного ключа для подписи кук
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI  # установка URI для базы данных SQLite
app.config[
    'SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS  # выключение оповещений при изменении моделей
app.config['UPLOADED_MUSIC_DEST'] = os.path.join(os.getcwd(), 'upload')  # задание пути для загружаемых файлов

music_uploads = UploadSet("music", AUDIO)  # создание UploadSet для музыкальных файлов
configure_uploads(app, music_uploads)  # конфигурирование загрузки файлов для приложения

db = SQLAlchemy(app)  # создание объекта для работы с базой данных
migrate = Migrate(app, db)  # создание объекта для миграции базы данных
login_manager = LoginManager(app)  # создание объекта для авторизации пользователей
login_manager.login_view = 'login'  # указание вида для авторизации

from app import models, routes  # импортирование модулей из пакета app

from app.models import User  # импортирование модели User из модуля models


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))  # функция для получения текущего пользователя при авторизации
