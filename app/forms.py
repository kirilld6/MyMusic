# Импорт необходимых библиотек
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from .models import User


# Содержит поля для ввода имени пользователя, пароля
class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])


# Содержит поля для ввода имени пользователя, адреса электронной почты,
# пароля и подтверждения пароля.
class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    email = StringField('Адрес электронной почты', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Подтвердите пароль',
                                     validators=[DataRequired(),
                                                 EqualTo('password', message='Пароли должны совпадать')])

    def validate_username(self, username):
        # Проверяет, существует ли пользователь с таким именем в базе данных.
        # Если пользователь уже существует, то вызывает исключение ValidationError.

        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Пожалуйста, используйте другое имя пользователя.')

    def validate_email(self, email):

        # Проверяет, существует ли пользователь с таким адресом электронной почты в базе данных.
        # Если пользователь уже существует, то вызывает исключение ValidationError.

        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Пожалуйста, используйте другой адрес электронной почты.')

# Форма для загрузки файлов на сервер.
class UploadForm(FlaskForm):
    file = FileField('Выберите файл для загрузки', validators=[FileRequired()])
    title = StringField('Название', validators=[DataRequired()])
    artist = StringField('Исполнитель', validators=[DataRequired()])
