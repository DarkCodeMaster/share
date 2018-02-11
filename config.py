import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = 'Hello World'
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PROT = 25
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'rfy1997@qq.com'
    MAIL_PASSWORD = 'weaker9527'
    MAIL_DEBUG = True
    FLASKY_MAIL_SUBJECT_PREFIX = '[Share]'
    FLASKY_MAIL_SENDER = 'Share Admin <rfy1997@qq.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

class TestingConfig(Config):
    pass

class ProductionConfig(Config):
    pass

config = {
    'development' : DevelopmentConfig,
    'testing' : TestingConfig,
    'production' : ProductionConfig,

    'default' : DevelopmentConfig
}
