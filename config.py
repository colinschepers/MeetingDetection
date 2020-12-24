import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DATA_PATH = os.path.join(basedir, 'data')
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
    pass


configs_types = {
    'default': Config,
    'development': DevelopmentConfig,
    'production': ProductionConfig
}

config = configs_types[os.getenv('CONFIG', 'default')]()