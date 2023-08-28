import unittest

from acai_aws.apigateway.endpoint import Endpoint
from acai_aws.apigateway.exception import ApiException
from acai_aws.apigateway.request import Request
from acai_aws.apigateway.resolver import Resolver

from tests.mocks.apigateway import mock_request


class ResolverTest(unittest.TestCase):
    base_path = 'unit-test/v1'
    handler_path = 'tests/mocks/apigateway/resolver/directory_handlers'
    bad_method_request = mock_request.get_basic_post_bad_method()
    basic_request = mock_request.get_basic_post()
    dynamic_request = mock_request.get_dynamic_post()
    bad_dynamic_request = mock_request.get_bad_dynamic_post()
    bad_dynamic_request_get = mock_request.get_bad_dynamic_get()
    no_dynamic_request = mock_request.get_no_dynamic_post()
    expected_path_params = {'id': '1'}

    def test_basic_resolve_works(self):
        request = Request(self.basic_request)
        resolver = Resolver(base_path=self.base_path, handlers=self.handler_path)
        endpoint = resolver.get_endpoint(request)
        self.assertTrue(isinstance(endpoint, Endpoint))

    def test_dynamic_resolve_checks_bad_route_throws_exception(self):
        request = Request(self.bad_dynamic_request)
        resolver = Resolver(base_path=self.base_path, handlers=self.handler_path)
        try:
            resolver.get_endpoint(request)
            self.assertTrue(False)
        except ApiException as api_error:
            self.assertEqual('no route found; requested dynamic route does not match endpoint route definition', api_error.message)

    def test_dynamic_resolve_checks_bad_route_definition_throws_exception(self):
        request = Request(self.bad_dynamic_request_get)
        resolver = Resolver(base_path=self.base_path, handlers=self.handler_path)
        try:
            resolver.get_endpoint(request)
            self.assertTrue(False)
        except ApiException as api_error:
            self.assertEqual('no route found; endpoint does not have proper variables in required_route', api_error.message)

    def test_dynamic_resolve_checks_no_route_throws_exception(self):
        request = Request(self.no_dynamic_request)
        resolver = Resolver(base_path=self.base_path, handlers=self.handler_path)
        try:
            resolver.get_endpoint(request)
            self.assertTrue(False)
        except ApiException as api_error:
            self.assertEqual('no route found; endpoint does have required_route configured', api_error.message)

    def test_basic_request_with_bad_method(self):
        request = Request(self.bad_method_request)
        resolver = Resolver(base_path=self.base_path, handlers=self.handler_path)
        try:
            resolver.get_endpoint(request)
            self.assertTrue(False)
        except ApiException as api_error:
            self.assertEqual('method not allowed', api_error.message)

    def test_get_endpoint_from_cache_works(self):
        request = Request(self.basic_request)
        resolver = Resolver(base_path=self.base_path, handlers=self.handler_path)
        self.assertEqual(0, resolver.cache_misses)
        resolver.get_endpoint(request)
        self.assertEqual(1, resolver.cache_misses)
        resolver.get_endpoint(request)
        self.assertEqual(1, resolver.cache_misses)
