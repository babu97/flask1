import os
basedir = os.path.abspath(os.path.dirname(__file__))
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'kipkulei'
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.mailgun.org')
    MAIL_PORT  = int(os.environ.get('MAIL_PORT' , '587'))
    MAILGUN_KEY = os.environ.get('MAILGUN_KEY')
    MAILGUN_DOMAIN = os.environ.get('MAILGUN_DOMAIN')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') 
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') 
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'flasky Admin<admin@Rosetta.technology'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    FLASKY_POSTS_PER = 5
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SSL_REDIRECT = False
    FLASKY_FOLLOWERS_PER_PAGE= 50
    FLASKY_POSTS_PER_PGE=50

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABSE_URI') or 'sqlite:///' +os.path.join(basedir, 'data-dev.sqlite')

class TestingConfig(Config):

  TESTING = True
  SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URI') or 'sqlite:///'
  WTF_CSRF_ENABLED = False


class ProductionConfig(Config):

    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABSE_URI') or 'sqlite:///' +os.path.join(basedir, 'data.sqlite')


config = {

    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default' : DevelopmentConfig

}




