import unittest

from acai.apigateway.request import Request
from acai.apigateway.resolver.directory import Directory
from acai.apigateway.resolver.exception import ResolverException
from tests.mocks import mock_request


class DirectoryTest(unittest.TestCase):
    basic_request = mock_request.get_basic()
    nested_request = mock_request.get_basic_nested()
    init_request = mock_request.get_basic_init()
    dynamic_request = mock_request.get_dynamic()
    bad_route_request = mock_request.get_bad_route()
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
        self.assertEqual('tests/mocks/resolver/directory-handlers/nested_1/nested_2/basic.py', resolved_path)

    def test_default_init_routing(self):
        request = Request(self.init_request)
        resolved_path = self.directory_resolver.resolve(request)
        self.assertEqual('tests/mocks/resolver/directory-handlers/home/__init__.py', resolved_path)

    def test_dynamic_routing(self):
        request = Request(self.dynamic_request)
        resolved_path = self.directory_resolver.resolve(request)
        self.assertEqual('tests/mocks/resolver/directory-handlers/dynamic/_id_.py', resolved_path)

    def test_route_not_found_raises_resolver_exception(self):
        try:
            request = Request(self.bad_route_request)
            self.directory_resolver.resolve(request)
            self.assertTrue(False)
        except ResolverException as resolver_error:
            self.assertTrue(isinstance(resolver_error, ResolverException))
            self.assertEqual(resolver_error.code, 404)
            self.assertEqual(resolver_error.key_path, 'bad/route')
            self.assertEqual(resolver_error.message, 'route not found')
