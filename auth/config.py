import os


BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    HOST = "0.0.0.0"
    PORT = 8085
    DEBUG = False
    SECRET_KEY = "tritondevs"
    ENCRYPTION_ALGORITHM = 'HS256'
    MAIL_KEY = "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"
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class ProductionConfig(Config):
    POSTGRES_USER = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
    POSTGRES_DATABASE_NAME = 'triton_auth'
    SQLALCHEMY_DATABASE_URI = 'postgresql://%s:%s@%s/%s' % (
        POSTGRES_USER,
        POSTGRES_PASSWORD,
        POSTGRES_HOST,
        POSTGRES_DATABASE_NAME
        )


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'auth.db')


class TestingConfig(Config):
    TESTING = True
