import unittest

from acai_aws.apigateway.request import Request
from acai_aws.apigateway.response import Response
from acai_aws.apigateway.resolver.modes.directory import DirectoryModeResolver
from acai_aws.apigateway.exception import ApiException
from tests.mocks.apigateway import mock_request


class DirectoryModeResolverTest(unittest.TestCase):
    basic_request = mock_request.get_basic()
    nested_request = mock_request.get_basic_nested()
    init_request = mock_request.get_basic_init()
    dynamic_request = mock_request.get_dynamic()
    triple_request = mock_request.get_triple_post()
    bad_route_request = mock_request.get_bad_route()
    base_path = 'unit-test/v1'
    handler_path = 'tests/mocks/apigateway/resolver/directory_handlers'
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
        self.directory_resolver = DirectoryModeResolver(base_path=self.base_path, handlers=self.handler_path)

    def test_get_endpoint_module(self):
        request = Request(self.basic_request)
        response = Response()
        endpoint_module = self.directory_resolver.get_endpoint_module(request)
        self.assertTrue(hasattr(endpoint_module, 'post'))
        endpoint_returns = endpoint_module.post(request, response)
        self.assertEqual(str(self.expected_endpoint_return), str(endpoint_returns))

    def test_basic_get_file_and_import_path(self):
        request = Request(self.basic_request)
        file_path, import_path = self.directory_resolver._get_file_and_import_path(request.path)
        self.assertTrue('tests/mocks/apigateway/resolver/directory_handlers/basic.py' in file_path)
        self.assertEqual('tests.mocks.apigateway.resolver.directory_handlers.basic', import_path)

    def test_nested_get_file_and_import_path(self):
        request = Request(self.nested_request)
        file_path, import_path = self.directory_resolver._get_file_and_import_path(request.path)
        self.assertTrue('tests/mocks/apigateway/resolver/directory_handlers/nested_1/nested_2/basic.py' in file_path)
        self.assertEqual('tests.mocks.apigateway.resolver.directory_handlers.nested_1.nested_2.basic', import_path)

    def test_default_init_get_file_and_import_path(self):
        request = Request(self.init_request)
        file_path, import_path = self.directory_resolver._get_file_and_import_path(request.path)
        self.assertTrue('tests/mocks/apigateway/resolver/directory_handlers/home/__init__.py' in file_path)
        self.assertEqual('tests.mocks.apigateway.resolver.directory_handlers.home.__init__', import_path)

    def test_dynamic_get_file_and_import_path(self):
        request = Request(self.dynamic_request)
        file_path, import_path = self.directory_resolver._get_file_and_import_path(request.path)
        self.assertTrue('tests/mocks/apigateway/resolver/directory_handlers/dynamic/_id_.py' in file_path)
        self.assertEqual('tests.mocks.apigateway.resolver.directory_handlers.dynamic._id_', import_path)

    def test_file_and_import_path_not_found_raises_resolver_exception(self):
        try:
            request = Request(self.bad_route_request)
            self.directory_resolver._get_file_and_import_path(request.path)
            self.assertTrue(False)
        except ApiException as resolver_error:
            self.assertTrue(isinstance(resolver_error, ApiException))
            self.assertEqual(resolver_error.code, 404)
            self.assertEqual(resolver_error.message, 'route not found')

    def test_triple_dynamic_get_file_and_import_path(self):
        request = Request(self.triple_request)
        file_path, import_path = self.directory_resolver._get_file_and_import_path(request.path)
        self.assertTrue('tests/mocks/apigateway/resolver/directory_handlers/triple/_coordinates.py' in file_path)
        self.assertEqual('tests.mocks.apigateway.resolver.directory_handlers.triple._coordinates', import_path)

    def test_single_nested_dynamic_get_file_and_import_path(self):
        dynamic_nested_request = mock_request.get_dynamic_nested_request_get('user/1')
        request = Request(dynamic_nested_request)
        file_path, import_path = self.directory_resolver._get_file_and_import_path(request.path)
        self.assertTrue('tests/mocks/apigateway/resolver/directory_handlers/user/_user_id/__init__.py' in file_path)
        self.assertEqual('tests.mocks.apigateway.resolver.directory_handlers.user._user_id.__init__', import_path)

    def test_double_nested_dynamic_get_file_and_import_path(self):
        dynamic_nested_request = mock_request.get_dynamic_nested_request_get('user/1/item')
        request = Request(dynamic_nested_request)
        file_path, import_path = self.directory_resolver._get_file_and_import_path(request.path)
        self.assertTrue('tests/mocks/apigateway/resolver/directory_handlers/user/_user_id/item/__init__.py' in file_path)
        self.assertEqual('tests.mocks.apigateway.resolver.directory_handlers.user._user_id.item.__init__', import_path)

    def test_triple_nested_dynamic_get_file_and_import_path(self):
        dynamic_nested_request = mock_request.get_dynamic_nested_request_get('user/1/item/a')
        request = Request(dynamic_nested_request)
        file_path, import_path = self.directory_resolver._get_file_and_import_path(request.path)
        self.assertTrue('tests/mocks/apigateway/resolver/directory_handlers/user/_user_id/item/_item_id.py' in file_path)
        self.assertEqual('tests.mocks.apigateway.resolver.directory_handlers.user._user_id.item._item_id', import_path)

