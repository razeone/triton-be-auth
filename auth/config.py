import os


BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    HOST = "0.0.0.0"
    PORT = 8085
    SECRET_KEY = "tritondevs"
    ENCRYPTION_ALGORITHM = 'HS256'
    REDIS_HOST = "localhost"
    REDIS_PORT = 6379
    MAIL_KEY = "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"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEBUG = False


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
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'auth.db')
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
