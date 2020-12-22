import logging.config
from config import config


def create_logger(config):
    logging.config.fileConfig(config.LOGGING_CONF_FILE)
    for logger_name, log_level in config.LOG_LEVELS.items():
        logging.getLogger(logger_name).setLevel(log_level)
    return logging.getLogger(config.LOGGER_NAME)


logger = create_logger(config)