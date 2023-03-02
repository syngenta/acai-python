import unittest

from acai.apigateway.request import Request
from acai.apigateway.router.exception import RouteException
from acai.apigateway.resolver.directory import Directory
from tests.mocks import mock_request


class DirectoryResolverTest(unittest.TestCase):
    basic_request = mock_request.get_basic()
    nested_request = mock_request.get_basic_nested()
    init_request = mock_request.get_basic_init()
    dynamic_request = mock_request.get_dynamic()
    bad_route_request = mock_request.get_bad_route()
    base_path = 'unit-test/v1'
    handler_path = 'tests/mocks/resolver/directory_handlers'

    def setUp(self):
        self.directory_resolver = Directory(base_path=self.base_path, handler_path=self.handler_path)

    def test_basic_routing(self):
        request = Request(self.basic_request)
        file_path, import_path = self.directory_resolver.get_file_and_import_path(request)
        self.assertEqual('tests/mocks/resolver/directory_handlers/basic.py', file_path)
        self.assertEqual('tests.mocks.resolver.directory_handlers.basic', import_path)

    def test_nested_routing(self):
        request = Request(self.nested_request)
        file_path, import_path = self.directory_resolver.get_file_and_import_path(request)
        self.assertEqual('tests/mocks/resolver/directory_handlers/nested_1/nested_2/basic.py', file_path)
        self.assertEqual('tests.mocks.resolver.directory_handlers.nested_1.nested_2.basic', import_path)

    def test_default_init_routing(self):
        request = Request(self.init_request)
        file_path, import_path = self.directory_resolver.get_file_and_import_path(request)
        self.assertEqual('tests/mocks/resolver/directory_handlers/home/__init__.py', file_path)
        self.assertEqual('tests.mocks.resolver.directory_handlers.home.__init__', import_path)

    def test_dynamic_routing(self):
        request = Request(self.dynamic_request)
        file_path, import_path = self.directory_resolver.get_file_and_import_path(request)
        self.assertEqual('tests/mocks/resolver/directory_handlers/dynamic/_id_.py', file_path)
        self.assertEqual('tests.mocks.resolver.directory_handlers.dynamic._id_', import_path)

    def test_route_not_found_raises_resolver_exception(self):
        try:
            request = Request(self.bad_route_request)
            self.directory_resolver.get_file_and_import_path(request)
            self.assertTrue(False)
        except RouteException as resolver_error:
            self.assertTrue(isinstance(resolver_error, RouteException))
            self.assertEqual(resolver_error.code, 404)
            self.assertEqual(resolver_error.key_path, 'bad/route')
            self.assertEqual(resolver_error.message, 'route not found')
