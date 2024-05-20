import unittest

from acai_aws.apigateway.openapi.input.validator import InputValidator


class MockInputArguments:

    def __init__(self):
        self.base = 'acai_aws/example'
        self.handlers = 'tests/mocks/apigateway/openapi/**/*.py'
        self.output = 'tests/mocks'
        self.format = 'json,yml'


class InputValidatorTest(unittest.TestCase):

    def setUp(self):
        self.validator = InputValidator()

    def test_validate_arguments_all_pass(self):
        try:
            inputs = MockInputArguments()
            self.validator.validate_arguments(inputs)
            self.assertTrue(True)
        except:
            self.assertTrue(False)

    def test_validate_arguments_glob_fails(self):
        try:
            inputs = MockInputArguments()
            inputs.handlers = 'tests/mocks/apigateway/openapi'
            self.validator.validate_arguments(inputs)
            self.assertTrue(False)
        except Exception as error:
            self.assertTrue(True)
            self.assertTrue('needs to be a glob pattern containing a "*.py"' in repr(error))

    def test_validate_arguments_directory_fails(self):
        try:
            inputs = MockInputArguments()
            inputs.output = 'tests/fail'
            self.validator.validate_arguments(inputs)
            self.assertTrue(False)
        except Exception as error:
            self.assertTrue(True)
            self.assertTrue('is not a valid directory path' in repr(error))
