import os
from unittest import TestCase, mock

from acai_aws.common import logger
from acai_aws.common.logger.decorator import log

def some_log_condition(*args, **_):
    if args[0] == 1:
        return True
    return False

@log()
def mock_func_simple(arg1, arg2, **kwargs):
    return {'args': [arg1, arg2], 'kwargs': kwargs}

@log(level='INFO')
def mock_func_level(arg1, arg2, **kwargs):
    return {'args': [arg1, arg2], 'kwargs': kwargs}

@log(level='INFO', condition=some_log_condition)
def mock_func_condition(arg1, arg2, **kwargs):
    return {'args': [arg1, arg2], 'kwargs': kwargs}


class LoggerTest(TestCase):

    @mock.patch.dict(os.environ, {'RUN_MODE': 'SEE-LOGS', 'LOG_STAGE_VARIABLE': 'STAGE', 'STAGE': 'local'})
    def test_logger_logs_simple_local_json(self):
        logger.log(level='ERROR', log={'error': 'test-simple'})
    
    @mock.patch.dict(os.environ, {'RUN_MODE': 'SEE-LOGS', 'LOG_STAGE_VARIABLE': 'STAGE', 'STAGE': 'local', 'LOG_LEVEL': 'INFO', 'LOG_FORMAT': 'INLINE'})
    def test_logger_logs_simple_local_inline(self):
        logger.log(level='INFO', log={'error': 'test-simple'})

    @mock.patch.dict(os.environ, {'RUN_MODE': 'SEE-LOGS'})
    def test_logger_logs_simple_non_local(self):
        logger.log(level='ERROR', log={'error': 'test-simple'})

    @mock.patch.dict(os.environ, {'RUN_MODE': 'SEE-LOGS', 'LOG_STAGE_VARIABLE': 'STAGE', 'STAGE': 'local'})
    def test_logger_logs_simple_local(self):
        logger.log(level='ERROR', log={'error': 'test-simple-local'})

    @mock.patch.dict(os.environ, {'RUN_MODE': 'SEE-LOGS', 'LOG_STAGE_VARIABLE': 'STAGE', 'STAGE': 'local'})
    def test_logger_logs_error_json(self):
        try:
            raise Exception('error-object')
        except Exception as error:
            logger.log(level='ERROR', log=error)
        
    @mock.patch.dict(os.environ, {'RUN_MODE': 'SEE-LOGS', 'LOG_STAGE_VARIABLE': 'STAGE', 'STAGE': 'local', 'LOG_FORMAT': 'INLINE'})
    def test_logger_logs_error_inline(self):
        try:
            raise Exception('error-object')
        except Exception as error:
            logger.log(level='ERROR', log=error)

    @mock.patch.dict(os.environ, {'RUN_MODE': 'SEE-LOGS', 'LOG_STAGE_VARIABLE': 'STAGE', 'STAGE': 'local'})
    def test_logger_logs_error_as_object(self):
        try:
            raise 'error-string'
        except Exception as error:
            logger.log(level='ERROR', log={'error': error, 'request': 'request'})

    @mock.patch.dict(os.environ, {'RUN_MODE': 'SEE-LOGS', 'LOG_STAGE_VARIABLE': 'STAGE', 'STAGE': 'local', 'LOG_LEVEL': 'ERROR'})
    def test_logger_logs_ignore_info(self):
        logger.log(level='INFO', log={'INFO': 'ignore'})

    @mock.patch.dict(os.environ, {'RUN_MODE': 'SEE-LOGS', 'LOG_STAGE_VARIABLE': 'STAGE', 'STAGE': 'local', 'LOG_LEVEL': 'INFO'})
    def test_logger_logs_see_info(self):
        logger.log(level='INFO', log={'INFO': 'see'})

    @mock.patch.dict(os.environ, {'RUN_MODE': 'SEE-LOGS', 'LOG_STAGE_VARIABLE': 'STAGE', 'STAGE': 'local', 'LOG_LEVEL': 'INFO'})
    def test_log_decorator(self):
        result = mock_func_simple(1, 2, test=True)
        self.assertDictEqual({'args': [1, 2], 'kwargs': {'test': True}}, result)

    @mock.patch.dict(os.environ, {'RUN_MODE': 'SEE-LOGS', 'LOG_STAGE_VARIABLE': 'STAGE', 'STAGE': 'local', 'LOG_LEVEL': 'ERROR'})
    def test_log_decorator_with_level(self):
        result = mock_func_level(1, 2, test=True)
        self.assertDictEqual({'args': [1, 2], 'kwargs': {'test': True}}, result)

    @mock.patch.dict(os.environ, {'RUN_MODE': 'SEE-LOGS', 'LOG_STAGE_VARIABLE': 'STAGE', 'STAGE': 'local', 'LOG_LEVEL': 'INFO'})
    def test_log_decorator_with_condition_logs(self):
        result = mock_func_condition(1, 2, test=True)
        self.assertDictEqual({'args': [1, 2], 'kwargs': {'test': True}}, result)

    @mock.patch.dict(os.environ, {'RUN_MODE': 'SEE-LOGS', 'LOG_STAGE_VARIABLE': 'STAGE', 'STAGE': 'local', 'LOG_LEVEL': 'INFO'})
    def test_log_decorator_with_condition_does_not_log(self):
        result = mock_func_condition(3, 2, test=True)
        self.assertDictEqual({'args': [3, 2], 'kwargs': {'test': True}}, result)

    @mock.patch.dict(os.environ, {'RUN_MODE': 'SEE-LOGS', 'LOG_STAGE_VARIABLE': 'STAGE', 'STAGE': 'local', 'LOG_LEVEL': 'ERROR'})
    def test_logger_handles_bad_level(self):
        logger.log(level='BAD', log={'INFO': 'ignore'})
    
    @mock.patch.dict(os.environ, {'RUN_MODE': 'SEE-LOGS', 'LOG_STAGE_VARIABLE': 'STAGE', 'STAGE': 'local', 'LOG_LEVEL': 'ERROR', 'LOG_FORMAT': 'BAD'})
    def test_logger_handles_bad_format(self):
        logger.log(level='INFO', log={'INFO': 'ignore'})

