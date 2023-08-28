import unittest

from acai_aws.apigateway.request import Request
from acai_aws.apigateway.response import Response
from acai_aws.apigateway.resolver.modes.mapping import MappingModeResolver
from acai_aws.apigateway.exception import ApiException

from tests.mocks.apigateway import mock_request


class MappingModeResolverTest(unittest.TestCase):
    basic_request = mock_request.get_basic()
    nested_request = mock_request.get_basic_nested()
    init_request = mock_request.get_basic_init()
    dynamic_request = mock_request.get_dynamic()
    bad_route_request = mock_request.get_bad_route()
    base_path = 'unit-test/v1'
    handler_mapping_preferred = {
        'basic': 'tests/mocks/apigateway/resolver/mapping_handlers/basic.py'
    }
    handler_mapping_leading_slashes = {
        '/basic': '/tests/mocks/apigateway/resolver/mapping_handlers/basic.py'
    }
    handler_mapping_base_path_leading_slashes = {
        '/unit-test/v1/basic': '/tests/mocks/apigateway/resolver/mapping_handlers/basic.py'
    }
    handler_mapping_base_path_mismatch_slashes = {
        'unit-test/v1/basic': '/tests/mocks/apigateway/resolver/mapping_handlers/basic.py'
    }
    handler_mapping = {
        '/': 'tests/mocks/apigateway/resolver/mapping_handlers/basic.py',
        'basic': 'tests/mocks/apigateway/resolver/mapping_handlers/basic.py',
        'home': 'tests/mocks/apigateway/resolver/mapping_handlers/home/__init__.py',
        'nested-1/nested-2/basic': 'tests/mocks/apigateway/resolver/mapping_handlers/nested_1/nested_2/basic.py',
        'dynamic/{id}': 'tests/mocks/apigateway/resolver/mapping_handlers/dynamic/_id.py'
    }

    def setUp(self):
        self.mapping_resolver = MappingModeResolver(base_path=self.base_path, handlers=self.handler_mapping)

    def test_get_file_and_import_path_module_with_preferred_mapping(self):
        mapping_resolver = MappingModeResolver(base_path=self.base_path, handlers=self.handler_mapping_preferred)
        request = Request(self.basic_request)
        file_path, import_path = mapping_resolver._get_file_and_import_path(request.path)
        self.assertTrue('tests/mocks/apigateway/resolver/mapping_handlers/basic.py' in file_path)
        self.assertEqual('tests.mocks.apigateway.resolver.mapping_handlers.basic', import_path)

    def test_get_file_and_import_path_module_with_dirty_mapping(self):
        mapping_resolver = MappingModeResolver(base_path=self.base_path, handlers=self.handler_mapping_leading_slashes)
        request = Request(self.basic_request)
        file_path, import_path = mapping_resolver._get_file_and_import_path(request.path)
        self.assertTrue('tests/mocks/apigateway/resolver/mapping_handlers/basic.py' in file_path)
        self.assertEqual('tests.mocks.apigateway.resolver.mapping_handlers.basic', import_path)

    def test_get_file_and_import_path_module_with_disgusting_mapping(self):
        mapping_resolver = MappingModeResolver(base_path=self.base_path, handlers=self.handler_mapping_base_path_leading_slashes)
        request = Request(self.basic_request)
        file_path, import_path = mapping_resolver._get_file_and_import_path(request.path)
        self.assertTrue('tests/mocks/apigateway/resolver/mapping_handlers/basic.py' in file_path)
        self.assertEqual('tests.mocks.apigateway.resolver.mapping_handlers.basic', import_path)

    def test_get_file_and_import_path_module_with_super_disgusting_mapping(self):
        mapping_resolver = MappingModeResolver(base_path=self.base_path, handlers=self.handler_mapping_base_path_mismatch_slashes)
        request = Request(self.basic_request)
        file_path, import_path = mapping_resolver._get_file_and_import_path(request.path)
        self.assertTrue('tests/mocks/apigateway/resolver/mapping_handlers/basic.py' in file_path)
        self.assertEqual('tests.mocks.apigateway.resolver.mapping_handlers.basic', import_path)

    def test_get_endpoint_module(self):
        request = Request(self.basic_request)
        response = Response()
        endpoint_module = self.mapping_resolver.get_endpoint_module(request)
        self.assertTrue(hasattr(endpoint_module, 'post'))
        endpoint_returns = endpoint_module.post(request, response)
        self.assertEqual({'mapping_basic': True}, endpoint_returns.raw)

    def test_get_file_and_import_path_module_nested_route(self):
        request = Request(self.nested_request)
        response = Response()
        endpoint_module = self.mapping_resolver.get_endpoint_module(request)
        self.assertTrue(hasattr(endpoint_module, 'post'))
        endpoint_returns = endpoint_module.post(request, response)
        self.assertDictEqual({'mapping_nested_2_basic': True}, endpoint_returns.raw)

    def test_get_file_and_import_path_module_home_route(self):
        request = Request(self.init_request)
        response = Response()
        endpoint_module = self.mapping_resolver.get_endpoint_module(request)
        self.assertTrue(hasattr(endpoint_module, 'post'))
        endpoint_returns = endpoint_module.post(request, response)
        self.assertDictEqual({'mapping_home_init': True}, endpoint_returns.raw)

    def test_get_file_and_import_path_module_dynamic_route(self):
        request = Request(self.dynamic_request)
        response = Response()
        endpoint_module = self.mapping_resolver.get_endpoint_module(request)
        self.assertTrue(hasattr(endpoint_module, 'post'))
        endpoint_returns = endpoint_module.post(request, response)
        self.assertDictEqual({'mapping_dynamic': True}, endpoint_returns.raw)

    def test_get_file_and_import_path_module_bad_route(self):
        request = Request(self.bad_route_request)
        try:
            self.mapping_resolver.get_endpoint_module(request)
            self.assertTrue(False)
        except ApiException as resolver_error:
            self.assertTrue(isinstance(resolver_error, ApiException))
            self.assertEqual(resolver_error.code, 404)
            self.assertEqual(resolver_error.message, 'route not found')

    def test_get_file_and_import_path_module_empty_route(self):
        variable_request = mock_request.get_dynamic_event(path='unit-test/v1/', method='post')
        request = Request(variable_request)
        response = Response()
        endpoint_module = self.mapping_resolver.get_endpoint_module(request)
        self.assertTrue(hasattr(endpoint_module, 'post'))
        endpoint_returns = endpoint_module.post(request, response)
        self.assertEqual({'mapping_basic': True}, endpoint_returns.raw)
