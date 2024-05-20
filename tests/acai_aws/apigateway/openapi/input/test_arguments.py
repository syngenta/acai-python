import unittest
from unittest.mock import patch

from acai_aws.apigateway.openapi.input.arguments import InputArguments


class InputArgumentsTest(unittest.TestCase):
    
    @patch('sys.argv', ['InputArguments', 'generate-openapi', '--base=acai_aws/example', '--handlers=tests/mocks/apigateway/openapi/**/*.py', '--output=tests/outputs', '--format=json,yml'])
    def test_full_class(self):
        input_args = InputArguments()
        self.assertEqual('acai_aws/example', input_args.base)
        self.assertEqual('tests/mocks/apigateway/openapi/**/*.py', input_args.handlers)
        self.assertEqual('tests/outputs', input_args.output)
        self.assertListEqual(['json', 'yml'], input_args.formats)