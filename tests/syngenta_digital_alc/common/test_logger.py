import os
from unittest import TestCase, mock

from syngenta_digital_alc.common import logger


@mock.patch.dict(os.environ, {'RUN_MODE': 'SEE-LOGS'})
class LoggerTest(TestCase):

    def test_logger_logs_simple(self):
        logger.log(level='ERROR', log={'error': 'test'}, trace=True)

    def test_logger_logs_error(self):
        try:
            raise Exception('error')
        except Exception as error:
            logger.log(level='ERROR', log=repr(error), trace=True)

    def test_logger_logs_error_as_object(self):
        try:
            raise 'error'
        except Exception as error:
            logger.log(level='ERROR', log={'error': repr(error), 'request': 'request'}, trace=True)
