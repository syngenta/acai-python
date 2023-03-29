import unittest

from acai.apigateway.request import Request
from acai.apigateway.response import Response
from acai.apigateway.resolver.modes.mapping import MappingModeResolver

from tests.mocks import mock_request


class MappingModeResolverTest(unittest.TestCase):
    basic_request = mock_request.get_basic()
    nested_request = mock_request.get_basic_nested()
    init_request = mock_request.get_basic_init()
    dynamic_request = mock_request.get_dynamic()
    bad_route_request = mock_request.get_bad_route()
    base_path = 'unit-test/v1'
    handler_mapping = {
        'basic': 'tests/mocks/resolver/mapping_handlers/basic.py'
    }
    handler_mapping_preferred = {
        'basic': 'tests/mocks/resolver/mapping_handlers/basic.py'
    }
    handler_mapping_dirty = {
        '/basic': '/tests/mocks/resolver/mapping_handlers/basic.py'
    }
    handler_mapping_disgusting = {
        '/unit-test/v1/basic': '/tests/mocks/resolver/mapping_handlers/basic.py'
    }
    handler_mapping_super_disgusting = {
        'unit-test/v1/basic': '/tests/mocks/resolver/mapping_handlers/basic.py'
    }
    expected_endpoint_return = {
        'hasErrors': False,
        'response': {
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': '*'
            },
            'statusCode': 200,
            'isBase64Encoded': False,
            'body': {
                'directory_basic': True
            }
        }
    }

    def setUp(self):
        self.mapping_resolver = MappingModeResolver(base_path=self.base_path, handler_mapping=self.handler_mapping)

    def test_get_file_and_import_path_module_with_preferred_mapping(self):
        mapping_resolver = MappingModeResolver(base_path=self.base_path, handler_mapping=self.handler_mapping_preferred)
        request = Request(self.basic_request)
        file_path, import_path = mapping_resolver._get_file_and_import_path(request.path)
        self.assertEqual('/opt/project/tests/mocks/resolver/mapping_handlers/basic.py', file_path)
        self.assertEqual('tests.mocks.resolver.mapping_handlers.basic', import_path)

    def test_get_file_and_import_path_module_with_dirty_mapping(self):
        mapping_resolver = MappingModeResolver(base_path=self.base_path, handler_mapping=self.handler_mapping_dirty)
        request = Request(self.basic_request)
        file_path, import_path = mapping_resolver._get_file_and_import_path(request.path)
        self.assertEqual('/opt/project/tests/mocks/resolver/mapping_handlers/basic.py', file_path)
        self.assertEqual('tests.mocks.resolver.mapping_handlers.basic', import_path)

    def test_get_file_and_import_path_module_with_disgusting_mapping(self):
        mapping_resolver = MappingModeResolver(base_path=self.base_path, handler_mapping=self.handler_mapping_disgusting)
        request = Request(self.basic_request)
        file_path, import_path = mapping_resolver._get_file_and_import_path(request.path)
        self.assertEqual('/opt/project/tests/mocks/resolver/mapping_handlers/basic.py', file_path)
        self.assertEqual('tests.mocks.resolver.mapping_handlers.basic', import_path)

    def test_get_file_and_import_path_module_with_super_disgusting_mapping(self):
        mapping_resolver = MappingModeResolver(base_path=self.base_path, handler_mapping=self.handler_mapping_super_disgusting)
        request = Request(self.basic_request)
        file_path, import_path = mapping_resolver._get_file_and_import_path(request.path)
        self.assertEqual('/opt/project/tests/mocks/resolver/mapping_handlers/basic.py', file_path)
        self.assertEqual('tests.mocks.resolver.mapping_handlers.basic', import_path)

    def test_get_endpoint_module(self):
        request = Request(self.basic_request)
        response = Response()
        endpoint_module = self.mapping_resolver.get_endpoint_module(request)
        self.assertTrue(hasattr(endpoint_module, 'post'))
        endpoint_returns = endpoint_module.post(request, response)
        self.assertEqual(str(self.expected_endpoint_return), str(endpoint_returns))
