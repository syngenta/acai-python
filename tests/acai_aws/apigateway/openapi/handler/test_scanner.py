import os
import unittest

from acai_aws.apigateway.openapi.handler.scanner import HandlerScanner


class HandlerScannerTest(unittest.TestCase):
    handler_path = 'tests/mocks/apigateway/openapi/**/*.py'

    def setUp(self):
        self.scanner = HandlerScanner(self.handler_path)

    def test_file_separator(self):
        assert self.scanner.file_separator == os.sep

    def test_handlers(self):
        assert self.scanner.handlers == self.handler_path

    def test_clean_path(self):
        dirty_path = '/dirty/path/'
        result = self.scanner.clean_path(dirty_path)
        assert result == 'dirty/path'

    def test_get_handler_file_paths(self):
        paths = self.scanner.get_handler_file_paths()
        self.assertListEqual([
            'tests/mocks/apigateway/openapi/default-output.py',
            'tests/mocks/apigateway/openapi/basic.py',
            'tests/mocks/apigateway/openapi/router.py',
            'tests/mocks/apigateway/openapi/nested_1/__init__.py',
            'tests/mocks/apigateway/openapi/nested_1/nested_2/_id.py',
            'tests/mocks/apigateway/openapi/nested_1/nested_2/resource.py',
            'tests/mocks/apigateway/openapi/nested_1/nested_2/__init__.py',
            'tests/mocks/apigateway/openapi/_dynamic/__init__.py'
        ],
            paths
        )
