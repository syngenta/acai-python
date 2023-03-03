import unittest

from acai.apigateway.endpoint import Endpoint
from acai.apigateway.exception import ApiException
from acai.apigateway.request import Request
from acai.apigateway.resolver import Resolver

from tests.mocks import mock_request


class ResolverTest(unittest.TestCase):
    base_path = 'unit-test/v1'
    handler_path = 'tests/mocks/resolver/directory_handlers'
    basic_request = mock_request.get_basic_post()

    def test_basic_resolve_works(self):
        request = Request(self.basic_request)
        resolver = Resolver(routing_mode='directory', base_path=self.base_path, handler_path=self.handler_path)
        endpoint = resolver.get_endpoint(request)
        self.assertTrue(isinstance(endpoint, Endpoint))

    def test_resolver_validates_base_path(self):
        try:
            Resolver()
        except ApiException as api_error:
            self.assertTrue(isinstance(api_error, ApiException))
            self.assertEqual('base_path is required', api_error.message)

    def test_resolver_validates_routing_mode_exists(self):
        try:
            Resolver(base_path=self.base_path)
        except ApiException as api_error:
            self.assertTrue(isinstance(api_error, ApiException))
            self.assertEqual('routing_mode is required; must be one of `directory` || `pattern` || `mapping`', api_error.message)

    def test_resolver_validates_routing_mode_is_one_of(self):
        try:
            Resolver(base_path=self.base_path, routing_mode='n/a')
        except ApiException as api_error:
            self.assertTrue(isinstance(api_error, ApiException))
            self.assertEqual('routing_mode must be one of `directory` || `pattern` || `mapping`', api_error.message)

    def test_resolver_validates_directory_routing_mode_handler_path(self):
        try:
            Resolver(base_path=self.base_path, routing_mode='directory')
        except ApiException as api_error:
            self.assertTrue(isinstance(api_error, ApiException))
            self.assertEqual('`directory` routing_mode must use handler_path kwarg', api_error.message)

    def test_resolver_validates_pattern_routing_mode_handler_pattern(self):
        try:
            Resolver(base_path=self.base_path, routing_mode='pattern')
        except ApiException as api_error:
            self.assertTrue(isinstance(api_error, ApiException))
            self.assertEqual('`pattern` routing_mode must use handler_pattern kwarg', api_error.message)

    def test_resolver_validates_pattern_routing_mode_handler_mapping(self):
        try:
            Resolver(base_path=self.base_path, routing_mode='mapping')
        except ApiException as api_error:
            self.assertTrue(isinstance(api_error, ApiException))
            self.assertEqual('`mapping` routing_mode must use handler_mapping kwarg', api_error.message)


