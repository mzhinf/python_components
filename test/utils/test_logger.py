from unittest import TestCase

from .. import logger


class TestLogger(TestCase):

    def test_logger(self):
        logger.debug('This is logging debug message')
        logger.info('This is logging info message')
        logger.warning('This is logging warning message')
        logger.error('This is logging error message')
        logger.critical('This is logging critical message')
