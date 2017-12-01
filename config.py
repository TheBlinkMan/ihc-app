import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SERVER_NAME = 'localhost:5000'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
    MAIL_SUBJECT_PREFIX = '[IHC-APP]'

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    db_path = os.path.join(basedir, 'data-dev.sqlite')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
            'sqlite:///' + db_path

class TestingConfig(Config):
    TESTING = True #Won't send emails
    db_path = os.path.join(basedir, 'data-test.sqlite')
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
            'sqlite:///' + db_path

class ProductionConfig(Config):
    db_path = os.path.join(basedir, 'data.sqlite')
    SQLALCHEMY_DATABASE_URI = os.environ.get('PRODUCTION_DATABASE_URL') or \
            'sqlite:///' + db_path

config = {
        'development' : DevelopmentConfig,
        'testing' : TestingConfig,
        'production' : ProductionConfig,
        'default' : DevelopmentConfig
        }
