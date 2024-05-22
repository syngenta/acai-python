import os
import unittest
from unittest.mock import patch

from acai_aws.apigateway.__main__ import generate_openapi


def make_directory(directory):
    try:
        os.mkdir(directory)
    except:
        pass


class MainTest(unittest.TestCase):

    def setUp(self):
        make_directory('tests/outputs')
        make_directory('tests/outputs/main')

    @patch('sys.argv', [
        '__main__',
        'generate-openapi',
        '--base=acai_aws/example',
        '--handlers=tests/mocks/apigateway/openapi/**/*.py',
        '--output=tests/outputs/main',
        '--format=json,yml',
        '--delete'
    ])
    def test_main(self):
        generate_openapi()
        self.assertTrue(os.path.exists('tests/outputs/main/openapi.yml'))
        self.assertTrue(os.path.exists('tests/outputs/main/openapi.json'))
