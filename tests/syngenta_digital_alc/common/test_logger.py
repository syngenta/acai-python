import os
from unittest import TestCase, mock

from syngenta_digital_alc.common import logger


class LoggerTest(TestCase):

    @mock.patch.dict(os.environ, {'RUN_MODE': 'SEE-LOGS'})
    def test_logger_logs_simple(self):
        logger.log(level='ERROR', log={'error': 'test-simple'}, trace=True)

    @mock.patch.dict(os.environ, {'RUN_MODE': 'SEE-LOGS', 'STAGE': 'local'})
    def test_logger_logs_simple_local(self):
        logger.log(level='ERROR', log={'error': 'test-simple-local'}, trace=True)

    @mock.patch.dict(os.environ, {'RUN_MODE': 'SEE-LOGS'})
    def test_logger_logs_error(self):
        try:
            raise Exception('error-object')
        except Exception as error:
            logger.log(level='ERROR', log=repr(error), trace=True)

    @mock.patch.dict(os.environ, {'RUN_MODE': 'SEE-LOGS'})
    def test_logger_logs_error_as_object(self):
        try:
            raise 'error-string'
        except Exception as error:
            logger.log(level='ERROR', log={'error': repr(error), 'request': 'request'}, trace=True)

    @mock.patch.dict(os.environ, {'RUN_MODE': 'SEE-LOGS', 'STAGE': 'local', 'LOG_LEVEL': 'ERROR'})
    def test_logger_logs_ignore_info(self):
        logger.log(level='INFO', log={'INFO': 'ignore'}, trace=True)

    @mock.patch.dict(os.environ, {'RUN_MODE': 'SEE-LOGS', 'STAGE': 'local', 'LOG_LEVEL': '3'})
    def test_logger_logs_ignore_info_numeric(self):
        logger.log(level='INFO', log={'INFO': 'ignore-numeric'}, trace=True)

    @mock.patch.dict(os.environ, {'RUN_MODE': 'SEE-LOGS', 'STAGE': 'local', 'LOG_LEVEL': 'INFO'})
    def test_logger_logs_see_info(self):
        logger.log(level='INFO', log={'INFO': 'see'}, trace=True)

    @mock.patch.dict(os.environ, {'RUN_MODE': 'SEE-LOGS', 'STAGE': 'local', 'LOG_LEVEL': '1'})
    def test_logger_logs_see_info_numeric(self):
        logger.log(level='INFO', log={'INFO': 'see-numeric'}, trace=True)
