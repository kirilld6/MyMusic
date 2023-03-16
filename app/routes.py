# Импорт необходимых библиотек
import os

from flask import render_template, flash, redirect, url_for, request, send_file
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from app.forms import RegistrationForm, LoginForm, UploadForm
from app import app
from .models import Song, User, Playlist


# Главная страница
@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')


# Страница с авторизированным пользователем
@app.route('/user_aut.html')
def user_aut():
    songs = Song.query.all()
    return render_template('user_aut.html', songs=songs)


# Регистрация пользователя
@app.route('/register', methods=['GET', 'POST'])
def register():
    from app import db
    form = RegistrationForm()
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not username or not password:
            flash('Пожалуйста, введите действительное имя пользователя и пароль.')
            return redirect(url_for('register', form=form))
        if User.query.filter_by(username=username).first():
            flash('Имя пользователя уже существует.')
            return redirect(url_for('register', form=form))
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Регистрация успешно выполнена!')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


# Авторизация пользователя
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        remember_me = bool(request.form.get('remember_me'))
        user = User.query.filter_by(username=username).first()
        if not user or not user.check_password(password):
            flash('Неверное имя пользователя или пароль')
            return redirect(url_for('login', form=form))
        login_user(user, remember=remember_me)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('user_aut')
        return redirect(next_page)

    return render_template('login.html', form=form)


# Выход пользователя из системы
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


# Загрузка файла на сервер
@login_required
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    from app import db
    form = UploadForm()
    if form.validate_on_submit():
        title = form.title.data
        artist = form.artist.data
        file = form.file.data
        if not title or not artist or not file:
            flash('Пожалуйста, заполните все поля и выберите файл для загрузки.')
            return redirect(url_for('upload'))
        song = Song(title=title, artist=artist, user=current_user, filename=secure_filename(file.filename))
        existing_song = Song.query.filter_by(title=title, artist=artist).first()
        if existing_song:
            # Обновляем существующую композицию
            existing_song.title = song.title
            db.session.merge(existing_song)
        else:
            # add new song
            db.session.add(song)
            current_user.like_song(song)
        # добавляем композицию в плейлист пользователя
        user_playlist = current_user.playlist
        user_playlist.songs.append(song)
        db.session.commit()
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(os.getcwd(), 'upload', filename))
            song.filename = filename
            song.filetype = file.content_type
            db.session.commit()
        flash('Композиция успешно загружена!')
        return redirect(url_for('playlist'))

    return render_template('upload.html', form=form)


# вывод всех пользователей из базы данных и отображения их в шаблоне 'users.html'.
@app.route('/users')
def users():
    users = User.query.all()
    return render_template('users.html', users=users)


# просмотр плейлиста определенного пользователя и отображения его в шаблоне 'view_playlist.html'.
@app.route('/playlist/<username>')
def view_playlist(username):
    user = User.query.filter_by(username=username).first_or_404()
    playlist = user.playlist
    return render_template('view_playlist.html', user=user, playlist=playlist)


# добавление песни в список понравившихся у текущего пользователя.
@app.route('/like_song/<int:song_id>', methods=['POST'])
@login_required
def like_song(song_id):
    from app import db
    song = Song.query.get_or_404(song_id)
    current_user.liked_songs.append(song)
    db.session.commit()
    flash('Вы добавили композицию в свой список понравившихся!')
    return redirect(request.referrer)


# запрос на удаление песни из списка понравившихся у текущего пользователя.
@app.route('/unlike_song/<int:song_id>', methods=['POST'])
@login_required 
def unlike_song(song_id):
    from app import db
    song = Song.query.get_or_404(song_id)
    current_user.liked_songs.remove(song)
    db.session.commit()
    flash('Вы удалили композицию из своего списка понравившихся!')
    return redirect(request.referrer)


# запрос на отображение всех песен, которые пользователь добавил в свой список понравившихся.
@app.route('/liked_songs')
@login_required
def liked_songs():
    songs = current_user.liked_songs
    return render_template('liked_songs.html', songs=songs)


# запрос на отображение плейлиста текущего пользователя и создание нового плейлиста, если его нет.
@app.route('/playlist')
@login_required
def playlist():
    from app import db

    if current_user.playlist is None:
        # Если плейлист не найден, создадим новый и сохраним его в базе данных
        my_playlist = Playlist()
        current_user.playlist = my_playlist
        db.session.add(my_playlist)
        db.session.commit()

    # Если пользователь является владельцем плейлиста, то можем отобразить его содержимое
    music_files = current_user.playlist.songs.all()
    return render_template('playlist.html', music_files=music_files)


# запрос на воспроизведение музыкального файла в браузере пользователя.
@app.route('/play/<filename>')
def play(filename):
    mimetype = ''
    if filename.endswith('.mp3'):
        mimetype = 'audio/mpeg'
    elif filename.endswith('.wav'):
        mimetype = 'audio/wav'
    return send_file(os.path.join(os.getcwd(), 'upload', filename), mimetype=mimetype)


# запрос на удаление музыкального файла из плейлиста текущего пользователя и базы данных.
@app.route('/delete/<filename>', methods=['GET'])
def delete(filename):
    from app import db
    song = Song.query.filter_by(filename=filename).first()
    if song:
        filepath = os.path.join(os.getcwd(), 'upload', filename)
        if os.path.exists(filepath):
            os.remove(filepath)
        db.session.delete(song)
        db.session.commit()
        flash(f'Файл "{filename}" успешно удален', 'success')
    else:
        flash(f'Файл "{filename}" не существует в базе данных', 'danger')
    return redirect(url_for('playlist'))
