import os


BASE_DIR = os.path.abspath(os.path.dirname(__file__))

HOST = "0.0.0.0"
PORT = 8085
DEBUG = True

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'auth.db')
SQLALCHEMY_TRACK_MODIFICATIONS = True
DATABASE_CONNECT_OPTIONS = {}

SECRET_KEY = "tritondevs"
ENCRYPTION_ALGORITHM = 'HS256'

