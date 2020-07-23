import logging
import sys

LOGGER_FORMATTER = '[%(asctime)s: %(processName)s/%(threadName)s] %(levelname)s: %(message)s'


def get_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(LOGGER_FORMATTER)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    file_handler = logging.FileHandler(filename='log.log', mode='a')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger
