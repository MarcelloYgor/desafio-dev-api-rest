
from urllib.parse import quote_plus

class Config(object):
    @property
    def SQLALCHEMY_DATABASE_URI(self):
        if 'sqlite' in self.DB_CONN:
            return f'{self.DB_CONN}{self.DB_HOST}'
        else:
            return f'{self.DB_CONN}{self.DB_USER}:{quote_plus(self.DB_PASSW)}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

class TestingConfig(Config):
    ENV = 'development'
    DEBUG = True
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    API_SECRET_KEY = 'segredo@123'
    DB_CONN = 'sqlite://'
    DB_HOST = '/./test.db'
    DB_PORT = ''
    DB_NAME = ''
    DB_USER = ''
    DB_PASSW = ''
