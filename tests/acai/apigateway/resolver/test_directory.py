import unittest

from acai.apigateway.request import Request
from acai.apigateway.resolver.directory import Directory
from acai.apigateway.response import Response
from tests.mocks import mock_request


class DirectoryTest(unittest.TestCase):
    basic_request = mock_request.get_basic()
    base_path = 'unit-test/v1'
    handler_path = 'tests/mocks/apigateway/directory-handlers'

    def setUp(self):
        self.directory_resolver = Directory(base_path=self.base_path, handler_path=self.handler_path)
        self.request = Request(self.basic_request)
        self.response = Response()
