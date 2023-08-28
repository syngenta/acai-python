import unittest

from acai_aws.apigateway.request import Request
from acai_aws.apigateway.response import Response
from acai_aws.apigateway.resolver.modes.pattern import PatternModeResolver
from acai_aws.apigateway.exception import ApiException
from tests.mocks.apigateway import mock_request


class PatternModeResolverTest(unittest.TestCase):
    basic_request = mock_request.get_basic()
    nested_request = mock_request.get_basic_nested()
    init_request = mock_request.get_basic_init()
    dynamic_request = mock_request.get_dynamic()
    bad_route_request = mock_request.get_bad_route()
    triple_request = mock_request.get_triple_post()
    base_path = 'unit-test/v1'
    pattern = 'tests/mocks/apigateway/resolver/pattern_handlers/**/*_controller.py'
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
                'basic_pattern': True
            }
        }
    }

    def setUp(self):
        self.pattern_resolver = PatternModeResolver(base_path=self.base_path, handlers=self.pattern)

    def test_get_endpoint_module(self):
        request = Request(self.basic_request)
        response = Response()
        endpoint_module = self.pattern_resolver.get_endpoint_module(request)
        self.assertTrue(hasattr(endpoint_module, 'post'))
        endpoint_returns = endpoint_module.post(request, response)
        self.assertEqual(str(self.expected_endpoint_return), str(endpoint_returns))

    def test_basic_get_file_and_import_path(self):
        request = Request(self.basic_request)
        file_path, import_path = self.pattern_resolver._get_file_and_import_path(request.path)
        self.assertTrue('tests/mocks/apigateway/resolver/pattern_handlers/basic/basic_controller.py' in file_path)
        self.assertEqual('tests.mocks.apigateway.resolver.pattern_handlers.basic.basic_controller', import_path)

    def test_nested_get_file_and_import_path(self):
        request = Request(self.nested_request)
        file_path, import_path = self.pattern_resolver._get_file_and_import_path(request.path)
        self.assertTrue('tests/mocks/apigateway/resolver/pattern_handlers/nested_1/nested_2/basic/basic_controller.py' in file_path)
        self.assertEqual('tests.mocks.apigateway.resolver.pattern_handlers.nested_1.nested_2.basic.basic_controller', import_path)

    def test_default_init_get_file_and_import_path(self):
        request = Request(self.init_request)
        file_path, import_path = self.pattern_resolver._get_file_and_import_path(request.path)
        self.assertTrue('tests/mocks/apigateway/resolver/pattern_handlers/home/home_controller.py' in file_path)
        self.assertEqual('tests.mocks.apigateway.resolver.pattern_handlers.home.home_controller', import_path)

    def test_dynamic_get_file_and_import_path(self):
        request = Request(self.dynamic_request)
        file_path, import_path = self.pattern_resolver._get_file_and_import_path(request.path)
        self.assertTrue('tests/mocks/apigateway/resolver/pattern_handlers/dynamic/_id_controller.py' in file_path)
        self.assertEqual('tests.mocks.apigateway.resolver.pattern_handlers.dynamic._id_controller', import_path)

    def test_file_and_import_path_not_found_raises_resolver_exception(self):
        try:
            request = Request(self.bad_route_request)
            self.pattern_resolver._get_file_and_import_path(request.path)
            self.assertTrue(False)
        except ApiException as resolver_error:
            self.assertTrue(isinstance(resolver_error, ApiException))
            self.assertEqual(resolver_error.code, 404)
            self.assertEqual(resolver_error.message, 'route not found')

    def test_triple_dynamic_get_file_and_import_path(self):
        request = Request(self.triple_request)
        file_path, import_path = self.pattern_resolver._get_file_and_import_path(request.path)
        self.assertTrue('tests/mocks/apigateway/resolver/pattern_handlers/triple/_coordinates_controller.py' in file_path)
        self.assertEqual('tests.mocks.apigateway.resolver.pattern_handlers.triple._coordinates_controller', import_path)

    def test_single_nested_dynamic_get_file_and_import_path(self):
        dynamic_nested_request = mock_request.get_dynamic_nested_request_get('user/1')
        request = Request(dynamic_nested_request)
        file_path, import_path = self.pattern_resolver._get_file_and_import_path(request.path)
        self.assertTrue('tests/mocks/apigateway/resolver/pattern_handlers/user/_user_id/_user_id_controller.py' in file_path)
        self.assertEqual('tests.mocks.apigateway.resolver.pattern_handlers.user._user_id._user_id_controller', import_path)

    def test_double_nested_dynamic_get_file_and_import_path(self):
        dynamic_nested_request = mock_request.get_dynamic_nested_request_get('user/1/item')
        request = Request(dynamic_nested_request)
        file_path, import_path = self.pattern_resolver._get_file_and_import_path(request.path)
        self.assertTrue('tests/mocks/apigateway/resolver/pattern_handlers/user/_user_id/item/item_controller.py' in file_path)
        self.assertEqual('tests.mocks.apigateway.resolver.pattern_handlers.user._user_id.item.item_controller', import_path)

    def test_triple_nested_dynamic_get_file_and_import_path(self):
        dynamic_nested_request = mock_request.get_dynamic_nested_request_get('user/1/item/a')
        request = Request(dynamic_nested_request)
        file_path, import_path = self.pattern_resolver._get_file_and_import_path(request.path)
        self.assertTrue('tests/mocks/apigateway/resolver/pattern_handlers/user/_user_id/item/_item_id_controller.py' in file_path)
        self.assertEqual('tests.mocks.apigateway.resolver.pattern_handlers.user._user_id.item._item_id_controller', import_path)
