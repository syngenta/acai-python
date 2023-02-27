import unittest

from acai.apigateway.request import Request
from acai.apigateway.resolver.directory import Directory
from tests.mocks import mock_request


class DirectoryTest(unittest.TestCase):
    basic_request = mock_request.get_basic()
    nested_request = mock_request.get_basic_nested()
    init_request = mock_request.get_basic_init()
    base_path = 'unit-test/v1'
    handler_path = 'tests/mocks/resolver/directory-handlers'

    def setUp(self):
        self.directory_resolver = Directory(base_path=self.base_path, handler_path=self.handler_path)

    def test_basic_routing(self):
        request = Request(self.basic_request)
        resolved_path = self.directory_resolver.resolve(request)
        self.assertEqual('tests/mocks/resolver/directory-handlers/basic.py', resolved_path)

    def test_nested_routing(self):
        request = Request(self.nested_request)
        resolved_path = self.directory_resolver.resolve(request)
        self.assertEqual('tests/mocks/resolver/directory-handlers/nested-1/nested-2/basic.py', resolved_path)

    def test_default_init_routing(self):
        request = Request(self.init_request)
        resolved_path = self.directory_resolver.resolve(request)
        self.assertEqual('tests/mocks/resolver/directory-handlers/home/__init__.py', resolved_path)
