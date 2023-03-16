# Импорт необходимых библиотек
import os
from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, app

# Определение таблицы для отношения "Многие-ко-Многим" между User и Song

likes = db.Table('likes',
                 db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                 db.Column('song_id', db.Integer, db.ForeignKey('song.id')))


# Модель User
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    songs = db.relationship('Song', backref='user', lazy='dynamic')
    liked_songs = db.relationship('Song', secondary='likes',
                                  backref=db.backref('liking_users', lazy='dynamic'))
    playlist = db.relationship('Playlist', backref='user', uselist=False)

    # Установка пароля с использованием хэша пароля
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Проверка, соответствует ли указанный пароль хэшу пароля
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Метод для добавления песни в понравившиеся песни пользователя
    def like_song(self, song):
        if not self.has_liked_song(song):
            self.liked_songs.append(song)

    # Метод для удаления песни из понравившихся песен пользователя
    def unlike_song(self, song):
        if self.has_liked_song(song):
            self.liked_songs.remove(song)

    # Метод для проверки, понравилась ли пользователю песня
    def has_liked_song(self, song):
        return self.liked_songs.filter(likes.c.song_id == song.id).count() > 0

    # Метод для проверки, понравилась ли пользователю песня
    def get_liked_songs(self):
        return self.liked_songs.all()

    def __repr__(self):
        return '<User {}>'.format(self.username)


# Модель Song
class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    artist = db.Column(db.String(140))
    filename = db.Column(db.String(256))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    filetype = db.Column(db.String(32))

    # Способ сохранения файла песни и установки атрибутов filename и filetype
    def save_file(self, file):
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        self.filename = filename
        self.filetype = file.content_type

    def __repr__(self):
        return '<Song {} by {}>'.format(self.title, self.artist)


# Модель Playlist
class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    songs = db.relationship('Song', secondary='playlist_song',
                            backref=db.backref('playlists', lazy='dynamic'), lazy='dynamic')
    playlist_song = db.Table('playlist_song',
                             db.Column('playlist_id', db.Integer, db.ForeignKey('playlist.id')),
                             db.Column('song_id', db.Integer, db.ForeignKey('song.id')))

    def __repr__(self):
        return '<Playlist {}>'.format(self.name)
