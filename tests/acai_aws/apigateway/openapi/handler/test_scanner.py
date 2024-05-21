import os
import unittest

from acai_aws.apigateway.openapi.handler.scanner import HandlerScanner


class HandlerScannerTest(unittest.TestCase):
    handler_path = 'tests/mocks/apigateway/openapi/**/*.py'

    def setUp(self):
        self.maxDiff = None
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
        assert len(paths) == 8
    
    def test_get_handler_file_no_directory(self):
        scanner = HandlerScanner('tests/mocks/apigateway/openapi')
        paths = scanner.get_handler_file_paths()
        assert len(paths) == 8
