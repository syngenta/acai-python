import json
import unittest

from acai.apigateway.request import Request
from acai.apigateway.response import Response
from acai.apigateway.resolver.modes.pattern import PatternModeResolver
from acai.apigateway.exception import ApiException
from tests.mocks import mock_request


class PatternMVVMModeResolverTest(unittest.TestCase):
    basic_request = mock_request.get_basic()
    nested_request = mock_request.get_basic_nested()
    init_request = mock_request.get_basic_init()
    dynamic_request = mock_request.get_dynamic()
    bad_route_request = mock_request.get_bad_route()
    base_path = 'unit-test/v1'
    mvvm_pattern = 'tests/mocks/resolver/pattern_handlers/mvvm/**/*_controller.py'
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
                'basic_mvvm_pattern': True
            }
        }
    }

    def setUp(self):
        self.mvvm_pattern_resolver = PatternModeResolver(base_path=self.base_path, handlers=self.mvvm_pattern)

    def test_get_endpoint_module(self):
        request = Request(self.basic_request)
        response = Response()
        endpoint_module = self.mvvm_pattern_resolver.get_endpoint_module(request)
        self.assertTrue(hasattr(endpoint_module, 'post'))
        endpoint_returns = endpoint_module.post(request, response)
        self.assertEqual(str(self.expected_endpoint_return), str(endpoint_returns))

    def test_basic_get_file_and_import_path(self):
        request = Request(self.basic_request)
        file_path, import_path = self.mvvm_pattern_resolver._get_file_and_import_path(request.path)
        self.assertTrue('tests/mocks/resolver/pattern_handlers/mvvm/basic/basic_controller.py' in file_path)
        self.assertEqual('tests.mocks.resolver.pattern_handlers.mvvm.basic.basic_controller', import_path)

    def test_nested_get_file_and_import_path(self):
        request = Request(self.nested_request)
        file_path, import_path = self.mvvm_pattern_resolver._get_file_and_import_path(request.path)
        self.assertTrue('tests/mocks/resolver/pattern_handlers/mvvm/nested_1/nested_2/basic/basic_controller.py' in file_path)
        self.assertEqual('tests.mocks.resolver.pattern_handlers.mvvm.nested_1.nested_2.basic.basic_controller', import_path)

    def test_default_init_get_file_and_import_path(self):
        request = Request(self.init_request)
        file_path, import_path = self.mvvm_pattern_resolver._get_file_and_import_path(request.path)
        self.assertTrue('tests/mocks/resolver/pattern_handlers/mvvm/home/home_controller.py' in file_path)
        self.assertEqual('tests.mocks.resolver.pattern_handlers.mvvm.home.home_controller', import_path)

    def test_dynamic_get_file_and_import_path(self):
        request = Request(self.dynamic_request)
        file_path, import_path = self.mvvm_pattern_resolver._get_file_and_import_path(request.path)
        self.assertTrue('tests/mocks/resolver/pattern_handlers/mvvm/dynamic/_id_controller.py' in file_path)
        self.assertEqual('tests.mocks.resolver.pattern_handlers.mvvm.dynamic._id_controller', import_path)

    def test_file_and_import_path_not_found_raises_resolver_exception(self):
        try:
            request = Request(self.bad_route_request)
            self.mvvm_pattern_resolver._get_file_and_import_path(request.path)
            self.assertTrue(False)
        except ApiException as resolver_error:
            self.assertTrue(isinstance(resolver_error, ApiException))
            self.assertEqual(resolver_error.code, 404)
            self.assertEqual(resolver_error.message, 'route not found')


class PatternMVCModeResolverTest(unittest.TestCase):
    basic_request = mock_request.get_basic()
    nested_request = mock_request.get_basic_nested()
    init_request = mock_request.get_basic_init()
    dynamic_request = mock_request.get_dynamic()
    bad_route_request = mock_request.get_bad_route()
    base_path = 'unit-test/v1'
    mvc_pattern = 'tests/mocks/resolver/pattern_handlers/mvc/**/*_controller.py'
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
                'basic_mvc_pattern': True
            }
        }
    }

    def setUp(self):
        self.mvc_pattern_resolver = PatternModeResolver(base_path=self.base_path, handlers=self.mvc_pattern)

    def test_get_endpoint_module(self):
        request = Request(self.basic_request)
        response = Response()
        endpoint_module = self.mvc_pattern_resolver.get_endpoint_module(request)
        self.assertTrue(hasattr(endpoint_module, 'post'))
        endpoint_returns = endpoint_module.post(request, response)
        self.assertEqual(str(self.expected_endpoint_return), str(endpoint_returns))

    def test_basic_get_file_and_import_path(self):
        request = Request(self.basic_request)
        file_path, import_path = self.mvc_pattern_resolver._get_file_and_import_path(request.path)
        self.assertTrue('tests/mocks/resolver/pattern_handlers/mvc/basic_controller.py' in file_path)
        self.assertEqual('tests.mocks.resolver.pattern_handlers.mvc.basic_controller', import_path)

    def test_nested_get_file_and_import_path(self):
        request = Request(self.nested_request)
        file_path, import_path = self.mvc_pattern_resolver._get_file_and_import_path(request.path)
        self.assertTrue('tests/mocks/resolver/pattern_handlers/mvc/nested_1/nested_2/basic_controller.py' in file_path)
        self.assertEqual('tests.mocks.resolver.pattern_handlers.mvc.nested_1.nested_2.basic_controller', import_path)

    def test_default_init_get_file_and_import_path(self):
        request = Request(self.init_request)
        file_path, import_path = self.mvc_pattern_resolver._get_file_and_import_path(request.path)
        self.assertTrue('tests/mocks/resolver/pattern_handlers/mvc/home_controller.py' in file_path)
        self.assertEqual('tests.mocks.resolver.pattern_handlers.mvc.home_controller', import_path)

    def test_dynamic_get_file_and_import_path(self):
        request = Request(self.dynamic_request)
        file_path, import_path = self.mvc_pattern_resolver._get_file_and_import_path(request.path)
        self.assertTrue('tests/mocks/resolver/pattern_handlers/mvc/dynamic/_id_controller.py' in file_path)
        self.assertEqual('tests.mocks.resolver.pattern_handlers.mvc.dynamic._id_controller', import_path)

    def test_file_and_import_path_not_found_raises_resolver_exception(self):
        try:
            request = Request(self.bad_route_request)
            self.mvc_pattern_resolver._get_file_and_import_path(request.path)
            self.assertTrue(False)
        except ApiException as resolver_error:
            self.assertTrue(isinstance(resolver_error, ApiException))
            self.assertEqual(resolver_error.code, 404)
            self.assertEqual(resolver_error.message, 'route not found')


class PatternConstantModeResolverTest(unittest.TestCase):
    basic_request = mock_request.get_basic()
    base_path = 'unit-test/v1'
    constant_pattern = 'tests/mocks/resolver/pattern_handlers/constant/**/*/endpoint.py'
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
                'basic_constant_pattern': True
            }
        }
    }

    def setUp(self):
        self.constant_pattern_resolver = PatternModeResolver(base_path=self.base_path, handlers=self.constant_pattern)

    def test_get_endpoint_module(self):
        request = Request(self.basic_request)
        response = Response()
        endpoint_module = self.constant_pattern_resolver.get_endpoint_module(request)
        self.assertTrue(hasattr(endpoint_module, 'post'))
        endpoint_returns = endpoint_module.post(request, response)
        self.assertEqual(str(self.expected_endpoint_return), str(endpoint_returns))


class PatternStraightModeResolverTest(unittest.TestCase):
    basic_request = mock_request.get_basic()
    base_path = 'unit-test/v1'
    straight_pattern = 'tests/mocks/resolver/pattern_handlers/straight/*.py'
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
                'basic_straight_pattern': True
            }
        }
    }

    def setUp(self):
        self.straight_pattern_resolver = PatternModeResolver(base_path=self.base_path, handlers=self.straight_pattern)

    def test_get_endpoint_module(self):
        request = Request(self.basic_request)
        response = Response()
        endpoint_module = self.straight_pattern_resolver.get_endpoint_module(request)
        self.assertTrue(hasattr(endpoint_module, 'post'))
        endpoint_returns = endpoint_module.post(request, response)
        self.assertEqual(str(self.expected_endpoint_return), str(endpoint_returns))
