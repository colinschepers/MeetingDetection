import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DATA_PATH = os.path.join(basedir, 'data')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(DATA_PATH, 'database.db')
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOGGING_CONF_FILE = 'logging.conf'
    LOGGER_NAME = 'meetings'
    LOG_LEVELS = {
        'app': 'DEBUG',
        'werkzeug': 'INFO',
        'transformers': 'WARNING'
    }


class DevelopmentConfig(Config):
    pass


class ProductionConfig(Config):
    SQLALCHEMY_ECHO = False


configs_types = {
    'default': Config,
    'development': DevelopmentConfig,
    'production': ProductionConfig
}

config = configs_types[os.getenv('CONFIG', 'default')]()