import unittest

from acai.apigateway.endpoint import Endpoint
from acai.apigateway.exception import ApiException
from acai.apigateway.request import Request
from acai.apigateway.resolver import Resolver

from tests.mocks import mock_request


class ResolverTest(unittest.TestCase):
    base_path = 'unit-test/v1'
    handler_path = 'tests/mocks/resolver/directory_handlers'
    bad_method_request = mock_request.get_basic_post_bad_method()
    basic_request = mock_request.get_basic_post()
    dynamic_request = mock_request.get_dynamic_post()
    bad_dynamic_request = mock_request.get_bad_dynamic_post()
    bad_dynamic_request_get = mock_request.get_bad_dynamic_get()
    no_dynamic_request = mock_request.get_no_dynamic_post()
    expected_path_params = {'id': '1'}

    def test_basic_resolve_works(self):
        request = Request(self.basic_request)
        resolver = Resolver(routing_mode='directory', base_path=self.base_path, handler_path=self.handler_path)
        endpoint = resolver.get_endpoint(request)
        self.assertTrue(isinstance(endpoint, Endpoint))

    def test_dynamic_resolve_works(self):
        request = Request(self.dynamic_request)
        resolver = Resolver(routing_mode='directory', base_path=self.base_path, handler_path=self.handler_path)
        resolver.get_endpoint(request)
        self.assertEqual('/unit-test/v1/dynamic/{id}', request.route)
        self.assertDictEqual(self.expected_path_params, request.path_params)

    def test_dynamic_resolve_checks_bad_route_throws_exception(self):
        request = Request(self.bad_dynamic_request)
        resolver = Resolver(routing_mode='directory', base_path=self.base_path, handler_path=self.handler_path)
        try:
            resolver.get_endpoint(request)
            self.assertTrue(False)
        except ApiException as api_error:
            self.assertEqual('no route found; requested dynamic route does not match endpoint route definition', api_error.message)

    def test_dynamic_resolve_checks_bad_route_definition_throws_exception(self):
        request = Request(self.bad_dynamic_request_get)
        resolver = Resolver(routing_mode='directory', base_path=self.base_path, handler_path=self.handler_path)
        try:
            resolver.get_endpoint(request)
            self.assertTrue(False)
        except ApiException as api_error:
            self.assertEqual('no route found; endpoint does not have proper variables in required_route', api_error.message)

    def test_dynamic_resolve_checks_no_route_throws_exception(self):
        request = Request(self.no_dynamic_request)
        resolver = Resolver(routing_mode='directory', base_path=self.base_path, handler_path=self.handler_path)
        try:
            resolver.get_endpoint(request)
            self.assertTrue(False)
        except ApiException as api_error:
            self.assertEqual('no route found; endpoint does have required_route configured', api_error.message)

    def test_basic_request_with_bad_method(self):
        request = Request(self.bad_method_request)
        resolver = Resolver(routing_mode='directory', base_path=self.base_path, handler_path=self.handler_path)
        try:
            resolver.get_endpoint(request)
            self.assertTrue(False)
        except ApiException as api_error:
            self.assertEqual('method not allowed', api_error.message)

    def test_resolver_validates_base_path(self):
        try:
            Resolver()
            self.assertTrue(False)
        except ApiException as api_error:
            self.assertTrue(isinstance(api_error, ApiException))
            self.assertEqual('base_path is required', api_error.message)

    def test_resolver_validates_routing_mode_exists(self):
        try:
            Resolver(base_path=self.base_path)
            self.assertTrue(False)
        except ApiException as api_error:
            self.assertTrue(isinstance(api_error, ApiException))
            self.assertEqual('routing_mode is required; must be one of `directory` || `pattern` || `mapping`', api_error.message)

    def test_resolver_validates_routing_mode_is_one_of(self):
        try:
            Resolver(base_path=self.base_path, routing_mode='n/a')
            self.assertTrue(False)
        except ApiException as api_error:
            self.assertTrue(isinstance(api_error, ApiException))
            self.assertEqual('routing_mode must be one of `directory` || `pattern` || `mapping`', api_error.message)

    def test_resolver_validates_directory_routing_mode_handler_path(self):
        try:
            Resolver(base_path=self.base_path, routing_mode='directory')
            self.assertTrue(False)
        except ApiException as api_error:
            self.assertTrue(isinstance(api_error, ApiException))
            self.assertEqual('`directory` routing_mode must use handler_path kwarg', api_error.message)

    def test_resolver_validates_pattern_routing_mode_handler_pattern(self):
        try:
            Resolver(base_path=self.base_path, routing_mode='pattern')
            self.assertTrue(False)
        except ApiException as api_error:
            self.assertTrue(isinstance(api_error, ApiException))
            self.assertEqual('`pattern` routing_mode must use handler_pattern kwarg', api_error.message)

    def test_resolver_validates_pattern_routing_mode_handler_mapping(self):
        try:
            Resolver(base_path=self.base_path, routing_mode='mapping')
            self.assertTrue(False)
        except ApiException as api_error:
            self.assertTrue(isinstance(api_error, ApiException))
            self.assertEqual('`mapping` routing_mode must use handler_mapping kwarg', api_error.message)
