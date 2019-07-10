import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'mail.proassurance.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '25'))
    MAIL_USE_TLS = \
      os.environ.get('MAIL_USE_TLS', 'false').lower() in ['false','off','0']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@example.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app): 
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = \
      os.environ.get('DEV_DATABASE_URL') or \
      'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

class TestingConfig(Config):
    TESTING = True
    # This specifies a default of an in-memory database,
    # if a testing database is not specified through an environment
    # variable.
    SQLALCHEMY_DATABASE_URI = \
      os.environ.get('TEST_DATABASE_URL') or \
      'sqlite://'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = \
      os.environ.get('DATABASE_URL') or \
      'sqlite:///' + os.path.join(basedir, 'data.sqlite')

# the 'default' configuration is also the 'development' configuration:
config = {
    'development' : DevelopmentConfig,
    'testing' : TestingConfig,
    'production' : ProductionConfig,
    'default' : DevelopmentConfig
}
