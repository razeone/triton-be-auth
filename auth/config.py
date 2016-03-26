import os


BASE_DIR = os.path.abspath(os.path.dirname(__file__))

HOST = "0.0.0.0"
PORT = 8085
DEBUG = False

POSTGRES_USER = os.environ.get('POSTGRES_USER', 'postgres')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'secret')
POSTGRES_HOST = 'localhost'
POSTGRES_DATABASE_NAME = os.environ.get('POSTGRES_DATABASE_NAME', 'triton_auth')


SQLALCHEMY_DATABASE_URI = 'postgresql://' + POSTGRES_USER + ':' + POSTGRES_PASSWORD + '@' + POSTGRES_HOST + '/' + POSTGRES_DATABASE_NAME

if DEBUG:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'auth.db')


SQLALCHEMY_TRACK_MODIFICATIONS = True


SECRET_KEY = "tritondevs"
ENCRYPTION_ALGORITHM = 'HS256'

