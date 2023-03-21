import json
import unittest

from acai.apigateway.router import Router

from tests.mocks import mock_request, mock_middleware


class RouterTest(unittest.TestCase):
    base_path = 'unit-test/v1'
    handler_path = 'tests/mocks/router/directory_handlers'
    schema_path = 'tests/mocks/openapi.yml'
    basic_event = mock_request.get_basic_post()
    raise_exception_event = mock_request.get_raised_exception_post()
    unhandled_exception_event = mock_request.get_unhandled_exception_post()
    expected_open_headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': '*'
    }

    def test_basic_directory_routing_works(self):
        router = Router(
            routing_mode='directory',
            base_path=self.base_path,
            handler_path=self.handler_path,
            schema=self.schema_path
        )
        result = router.route(self.basic_event, None)
        json_dict_response = json.loads(result['body'])
        self.assertFalse(result['isBase64Encoded'])
        self.assertEqual(200, result['statusCode'])
        self.assertDictEqual(self.expected_open_headers, result['headers'])
        self.assertDictEqual({"router_directory_basic": {"body_key": "body_value"}}, json_dict_response)

    def test_basic_directory_routing_works_no_schema_defined(self):
        router = Router(
            routing_mode='directory',
            base_path=self.base_path,
            handler_path=self.handler_path
        )
        result = router.route(self.basic_event, None)
        json_dict_response = json.loads(result['body'])
        self.assertFalse(result['isBase64Encoded'])
        self.assertEqual(200, result['statusCode'])
        self.assertDictEqual(self.expected_open_headers, result['headers'])
        self.assertDictEqual({"router_directory_basic": {"body_key": "body_value"}}, json_dict_response)

    def test_basic_directory_routing_works_with_raised_exception(self):
        router = Router(
            routing_mode='directory',
            base_path=self.base_path,
            handler_path=self.handler_path,
            schema=self.schema_path
        )
        result = router.route(self.raise_exception_event, None)
        json_dict_response = json.loads(result['body'])
        self.assertFalse(result['isBase64Encoded'])
        self.assertEqual(418, result['statusCode'])
        self.assertDictEqual(self.expected_open_headers, result['headers'])
        self.assertDictEqual({"errors": [{"key_path": "crazy_error", "message": "I am a teapot"}]}, json_dict_response)

    def test_basic_directory_routing_works_with_unhandled_exception(self):
        router = Router(
            routing_mode='directory',
            base_path=self.base_path,
            handler_path=self.handler_path,
            schema=self.schema_path
        )
        result = router.route(self.unhandled_exception_event, None)
        json_dict_response = json.loads(result['body'])
        self.assertFalse(result['isBase64Encoded'])
        self.assertEqual(500, result['statusCode'])
        self.assertDictEqual(self.expected_open_headers, result['headers'])
        self.assertDictEqual({'errors': [{'key_path': 'unknown', 'message': "name 'UnknownException' is not defined"}]}, json_dict_response)

    def test_basic_directory_routing_works_and_before_all_function_called(self):
        router = Router(
            routing_mode='directory',
            base_path=self.base_path,
            handler_path=self.handler_path,
            before_all=mock_middleware.mock_before_all,
            schema=self.schema_path
        )
        router.route(self.basic_event, None)
        self.assertTrue(mock_middleware.mock_before_all.has_been_called)

    def test_basic_directory_routing_works_and_after_all_function_called(self):
        router = Router(
            routing_mode='directory',
            base_path=self.base_path,
            handler_path=self.handler_path,
            after_all=mock_middleware.mock_after_all,
            schema=self.schema_path
        )
        router.route(self.basic_event, None)
        self.assertTrue(mock_middleware.mock_after_all.has_been_called)

    def test_basic_directory_routing_works_and_with_auth_function_called(self):
        router = Router(
            routing_mode='directory',
            base_path=self.base_path,
            handler_path=self.handler_path,
            with_auth=mock_middleware.mock_with_auth,
            schema=self.schema_path
        )
        router.route(self.basic_event, None)
        self.assertTrue(mock_middleware.mock_with_auth.has_been_called)

    def test_basic_directory_routing_works_and_on_error_function_called(self):
        router = Router(
            routing_mode='directory',
            base_path=self.base_path,
            handler_path=self.handler_path,
            on_error=mock_middleware.mock_on_error,
            schema=self.schema_path
        )
        router.route(self.raise_exception_event, None)
        self.assertTrue(mock_middleware.mock_on_error.has_been_called)
