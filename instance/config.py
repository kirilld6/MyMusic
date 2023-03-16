import os


UPLOADS_FOLDER = os.path.join(os.getcwd(), 'upload')

SECRET_KEY = 'my_secret_key_111_222_333'  # секретный ключ для подписи кук


basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                          'sqlite:///' + os.path.join(basedir, 'app.db')

SQLALCHEMY_TRACK_MODIFICATIONS = False
