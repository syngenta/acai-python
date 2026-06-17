import io
import json
import os
from contextlib import redirect_stdout
from unittest import TestCase, mock

from acai_aws.common import logger
from acai_aws.common.logger.decorator import log
from acai_aws.common.logger.common_logger import CommonLogger
from acai_aws.common.logger.redaction import RedactionFilter

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

    @mock.patch.dict(os.environ, {'RUN_MODE': 'SEE-LOGS', 'LOG_STAGE_VARIABLE': 'STAGE', 'STAGE': 'local', 'LOG_FORMAT': ' inline '})
    def test_logger_logs_error_inline_with_messy_env(self):
        logger.log(level='INFO', log={'message': 'inline-format'})

    @mock.patch.dict(os.environ, {'RUN_MODE': 'SEE-LOGS', 'LOG_STAGE_VARIABLE': 'STAGE', 'STAGE': 'local', 'LOG_FORMAT': 'JSON'})
    def test_logger_json_output(self):
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            logger.log(level='WARN', log={'json': True})
        log_output = buffer.getvalue().strip()
        self.assertNotIn('\n', log_output)
        parsed = json.loads(log_output)
        self.assertEqual('WARN', parsed['level'])
        self.assertEqual({'json': True}, parsed['log'])

    @mock.patch.dict(os.environ, {'RUN_MODE': 'SEE-LOGS', 'LOG_STAGE_VARIABLE': 'STAGE', 'STAGE': 'local', 'LOG_FORMAT': 'PRETTY'})
    def test_logger_pretty_output(self):
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            logger.log(level='WARN', log={'json': True})
        log_output = buffer.getvalue().strip()
        self.assertIn('\n', log_output)
        parsed = json.loads(log_output)
        self.assertEqual('WARN', parsed['level'])
        self.assertEqual({'json': True}, parsed['log'])

    @mock.patch.dict(os.environ, {'RUN_MODE': 'SEE-LOGS', 'LOG_STAGE_VARIABLE': 'STAGE', 'STAGE': 'local', 'LOG_FORMAT': 'INLINE'})
    def test_logger_inline_output(self):
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            logger.log(level='INFO', log={'inline': True})
        log_output = buffer.getvalue().strip()
        self.assertTrue(log_output.startswith('INFO|'))
        self.assertIn("inline': True", log_output)

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

    @mock.patch.dict(os.environ, {'RUN_MODE': 'SEE-LOGS', 'LOG_STAGE_VARIABLE': 'STAGE', 'STAGE': 'local', 'LOG_FORMAT': 'JSON'})
    def test_logger_accepts_canonical_warning(self):
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            logger.log(level='WARNING', log={'canonical': True})
        log_output = buffer.getvalue().strip()
        self.assertTrue(log_output, 'expected output for canonical WARNING level')
        parsed = json.loads(log_output)
        self.assertEqual('WARNING', parsed['level'])

    @mock.patch.dict(os.environ, {'RUN_MODE': 'SEE-LOGS', 'LOG_STAGE_VARIABLE': 'STAGE', 'STAGE': 'local', 'LOG_FORMAT': 'JSON', 'LOG_LEVEL': 'DEBUG'})
    def test_logger_accepts_debug_level(self):
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            logger.log(level='DEBUG', log={'debug': True})
        log_output = buffer.getvalue().strip()
        self.assertTrue(log_output, 'expected output for DEBUG level when LOG_LEVEL=DEBUG')
        parsed = json.loads(log_output)
        self.assertEqual('DEBUG', parsed['level'])

    @mock.patch.dict(os.environ, {'RUN_MODE': 'SEE-LOGS', 'LOG_STAGE_VARIABLE': 'STAGE', 'STAGE': 'local', 'LOG_FORMAT': 'JSON'})
    def test_logger_accepts_critical_level(self):
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            logger.log(level='CRITICAL', log={'critical': True})
        log_output = buffer.getvalue().strip()
        self.assertTrue(log_output, 'expected output for CRITICAL level')
        parsed = json.loads(log_output)
        self.assertEqual('CRITICAL', parsed['level'])

    @mock.patch.dict(os.environ, {'RUN_MODE': 'SEE-LOGS', 'LOG_STAGE_VARIABLE': 'STAGE', 'STAGE': 'local', 'LOG_LEVEL': 'ERROR', 'LOG_FORMAT': 'BAD'})
    def test_logger_handles_bad_format(self):
        logger.log(level='INFO', log={'INFO': 'ignore'})


class LoggerCallbackTest(TestCase):

    def setUp(self):
        self._saved_callbacks = list(CommonLogger._callbacks)
        CommonLogger.reset_callbacks()

    def tearDown(self):
        CommonLogger._callbacks = self._saved_callbacks

    @mock.patch.dict(os.environ, {'LOG_FORMAT': 'JSON', 'LOG_LEVEL': 'INFO'})
    def test_callback_runs_before_print(self):
        CommonLogger.register_callback(lambda record: {**record, 'log': {'replaced': True}})
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            logger.log(level='INFO', log={'email': 'ada@example.com'})
        parsed = json.loads(buffer.getvalue().strip())
        self.assertEqual({'replaced': True}, parsed['log'])

    @mock.patch.dict(os.environ, {'LOG_FORMAT': 'JSON', 'LOG_LEVEL': 'INFO'})
    def test_redaction_filter_runs_through_logger(self):
        CommonLogger.register_callback(RedactionFilter(keys=['email']))
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            logger.log(level='INFO', log={'email': 'ada@example.com', 'id': 1})
        parsed = json.loads(buffer.getvalue().strip())
        self.assertEqual('[REDACTED]', parsed['log']['email'])
        self.assertEqual(1, parsed['log']['id'])

    @mock.patch.dict(os.environ, {'LOG_FORMAT': 'JSON', 'LOG_LEVEL': 'INFO'})
    def test_callbacks_run_in_registration_order(self):
        CommonLogger.register_callback(lambda record: {**record, 'log': {'step': 'one'}})
        CommonLogger.register_callback(lambda record: {**record, 'log': {'step': 'two'}})
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            logger.log(level='INFO', log={'step': 'zero'})
        parsed = json.loads(buffer.getvalue().strip())
        self.assertEqual({'step': 'two'}, parsed['log'])

    def test_reset_callbacks_clears_registry(self):
        CommonLogger.register_callback(lambda record: record)
        self.assertEqual(1, len(CommonLogger._callbacks))
        CommonLogger.reset_callbacks()
        self.assertEqual(0, len(CommonLogger._callbacks))

    def test_register_callback_dedupes_equal_filters(self):
        CommonLogger.register_callback(RedactionFilter(keys=['email']))
        CommonLogger.register_callback(RedactionFilter(keys=['email']))
        self.assertEqual(1, len(CommonLogger._callbacks))

    def test_register_callback_keeps_distinct_filters(self):
        CommonLogger.register_callback(RedactionFilter(keys=['email']))
        CommonLogger.register_callback(RedactionFilter(keys=['phone']))
        self.assertEqual(2, len(CommonLogger._callbacks))

    def test_common_logger_is_singleton(self):
        self.assertIs(CommonLogger(), CommonLogger())
