import logging
import logging.config
from backend import config


def initialize_logger():
    """
    Initializes logger.
    If there is no log path, then we must be running on heroku. No log path needed because heroku reads default output.
    :return: 
    """
    if config.logger_path is None:
        logging.basicConfig()
    log = logging.getLogger(config.logger_name)
    if config.logger_path is not None:
        handler = logging.FileHandler(config.logger_path)
        formatter = logging.Formatter(
            '%(asctime)s %(levelname)s %(message)s', "%Y-%m-%d %H:%M:%S")
        handler.setFormatter(formatter)
        log.addHandler(handler)
    log.setLevel(logging.DEBUG)
    return log

logger = initialize_logger()
