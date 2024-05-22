import unittest
from unittest.mock import patch

from acai_aws.apigateway.openapi.input.arguments import InputArguments


class InputArgumentsTest(unittest.TestCase):

    @patch('sys.argv', [
        'InputArguments',
        'generate-openapi',
        '--base=acai_aws/example',
        '--handlers=tests/mocks/apigateway/openapi/**/*.py',
        '--output=tests/outputs/arguments',
        '--format=json,yml',
        '--delete'
    ])
    def test_full_class(self):
        input_args = InputArguments()
        self.assertEqual('acai_aws/example', input_args.base)
        self.assertEqual('tests/mocks/apigateway/openapi/**/*.py', input_args.handlers)
        self.assertEqual('tests/outputs/arguments', input_args.output)
        self.assertListEqual(['json', 'yml'], input_args.formats)
        self.assertTrue(input_args.delete)
