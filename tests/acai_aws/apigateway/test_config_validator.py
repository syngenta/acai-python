import unittest

from acai_aws.apigateway.config_validator import ConfigValidator
from acai_aws.apigateway.exception import ApiException


class ConfigValidatorTest(unittest.TestCase):

    def test_config_validator_validates_all_passing(self):
        try:
            ConfigValidator.validate(
                base_path='some/path',
                handlers={'route': 'file/path.py'},
                schema='path/to/schema',
                auto_validate=True,
                validate_response=True,
                cache_size=128,
                cache_mode='all'
            )
            # alternative options
            ConfigValidator.validate(
                base_path='some/path',
                handlers='some/path',
                schema={'json_schema': True},
                auto_validate=False,
                validate_response=False,
                cache_size=None
            )
            self.assertTrue(True)
        except ApiException as api_error:
            print(api_error.message)
            self.assertTrue(False)

    def test_config_validator_validates_base_path(self):
        try:
            ConfigValidator.validate(**{})
        except ApiException as api_error:
            self.assertTrue(isinstance(api_error, ApiException))
            self.assertEqual('base_path string is required', api_error.message)

    def test_config_validator_validates_routing_handlers_is_required(self):
        try:
            ConfigValidator.validate(base_path='some/path')
            self.assertTrue(False)
        except ApiException as api_error:
            self.assertTrue(isinstance(api_error, ApiException))
            self.assertEqual('handlers is required; must be glob pattern string or dictionary mapping {route: file_path}', api_error.message)

    def test_config_validator_validates_routing_handlers_are_appropriate(self):
        try:
            ConfigValidator.validate(base_path='some/path', handlers=1)
            self.assertTrue(False)
        except ApiException as api_error:
            self.assertTrue(isinstance(api_error, ApiException))
            self.assertEqual('handlers is required; must be glob pattern string or dictionary mapping {route: file_path}', api_error.message)

    def test_config_validator_validates_routing_schema_is_appropriate(self):
        try:
            ConfigValidator.validate(base_path='some/path', handlers={'route': 'file/path.py'}, schema=1)
            self.assertTrue(False)
        except ApiException as api_error:
            self.assertTrue(isinstance(api_error, ApiException))
            self.assertEqual('schema should either be file path string or json-schema style dictionary', api_error.message)

    def test_config_validator_validates_routing_auto_validate_is_appropriate(self):
        try:
            ConfigValidator.validate(base_path='some/path', handlers={'route': 'file/path.py'}, auto_validate=1)
            self.assertTrue(False)
        except ApiException as api_error:
            self.assertTrue(isinstance(api_error, ApiException))
            self.assertEqual('auto_validate should be a boolean', api_error.message)

    def test_config_validator_validates_routing_validate_response_is_appropriate(self):
        try:
            ConfigValidator.validate(base_path='some/path', handlers={'route': 'file/path.py'}, validate_response=1)
            self.assertTrue(False)
        except ApiException as api_error:
            self.assertTrue(isinstance(api_error, ApiException))
            self.assertEqual('validate_response should be a boolean', api_error.message)

    def test_config_validator_validates_routing_verbose_logging_is_appropriate(self):
        try:
            ConfigValidator.validate(base_path='some/path', handlers={'route': 'file/path.py'}, verbose_logging=1)
            self.assertTrue(False)
        except ApiException as api_error:
            self.assertTrue(isinstance(api_error, ApiException))
            self.assertEqual('verbose_logging should be a boolean', api_error.message)

    def test_config_validator_validates_routing_cache_size_is_appropriate(self):
        try:
            ConfigValidator.validate(base_path='some/path', handlers={'route': 'file/path.py'}, cache_size='1')
            self.assertTrue(False)
        except ApiException as api_error:
            self.assertTrue(isinstance(api_error, ApiException))
            self.assertEqual('cache_size should be an int (0 for unlimited size) or None (to disable route caching)', api_error.message)

    def test_config_validator_validates_routing_cache_mode_is_appropriate(self):
        try:
            ConfigValidator.validate(base_path='some/path', handlers={'route': 'file/path.py'}, cache_mode='bad')
            self.assertTrue(False)
        except ApiException as api_error:
            self.assertTrue(isinstance(api_error, ApiException))
            self.assertEqual('cache_mode should be a string of the one of the following values: all, static-only, dynamic-only', api_error.message)
