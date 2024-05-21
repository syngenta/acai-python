import os
import unittest
from unittest.mock import patch

from acai_aws.apigateway.__main__ import generate_openapi


class MainTest(unittest.TestCase):

    @patch('sys.argv', [
        '__main__',
        'generate-openapi',
        '--base=acai_aws/example',
        '--handlers=tests/mocks/apigateway/openapi/**/*.py',
        '--output=tests/outputs',
        '--format=json,yml'
    ])
    def test_main(self):
        generate_openapi()
        self.assertTrue(os.path.exists('tests/outputs/openapi.yml'))
        self.assertTrue(os.path.exists('tests/outputs/openapi.json'))
