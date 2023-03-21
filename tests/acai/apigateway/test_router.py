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
    mock_request = mock_request
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

    def test_requirements_decorator_works_and_passes_proper_body_request(self):
        dynamic_event = self.mock_request.get_dynamic_event(
            headers={'content-type': 'application/json'},
            path='unit-test/v1/nested/reqs',
            proxy='nested/reqs',
            method='post',
            body={
                'name': 'unit-test',
                'email': 'unit@email.com',
                'phone': 1234567890,
                'active': True
            }
        )
        router = Router(
            routing_mode='directory',
            base_path=self.base_path,
            handler_path=self.handler_path,
            schema=self.schema_path
        )
        result = router.route(dynamic_event, None)
        self.assertEqual(200, result['statusCode'])

    def test_requirements_decorator_works_and_fails_improper_body_request(self):
        dynamic_event = self.mock_request.get_dynamic_event(
            headers={'content-type': 'application/json'},
            path='unit-test/v1/nested/reqs',
            proxy='nested/reqs',
            method='post',
            body={
                'name': 'unit-test',
                'email': 'unit@email.com',
                'phone': '1234567890',
                'active': True
            }
        )
        router = Router(
            routing_mode='directory',
            base_path=self.base_path,
            handler_path=self.handler_path,
            schema=self.schema_path
        )
        result = router.route(dynamic_event, None)
        self.assertEqual(400, result['statusCode'])
        json_dict_response = json.loads(result['body'])
        self.assertDictEqual({'errors': [{'key_path': 'phone', 'message': "'1234567890' is not of type 'number'"}]}, json_dict_response)

    def test_requirements_decorator_works_and_passes_proper_query_request(self):
        dynamic_event = self.mock_request.get_dynamic_event(
            headers={'content-type': 'application/json'},
            path='unit-test/v1/nested/reqs',
            proxy='nested/reqs',
            method='get',
            query={
                'auth_id': 'some-id',
                'email': 'some@email.com',
                'name': 'unit-test'
            }
        )
        router = Router(
            routing_mode='directory',
            base_path=self.base_path,
            handler_path=self.handler_path,
            schema=self.schema_path
        )
        result = router.route(dynamic_event, None)
        self.assertEqual(200, result['statusCode'])
        self.assertDictEqual(self.expected_open_headers, result['headers'])

    def test_requirements_decorator_works_and_fails_improper_query_request_missing_required(self):
        dynamic_event = self.mock_request.get_dynamic_event(
            headers={'content-type': 'application/json'},
            path='unit-test/v1/nested/reqs',
            proxy='nested/reqs',
            method='get',
            query={
                'email': 'some@email.com',
                'name': 'unit-test'
            }
        )
        router = Router(
            routing_mode='directory',
            base_path=self.base_path,
            handler_path=self.handler_path
        )
        result = router.route(dynamic_event, None)
        self.assertEqual(400, result['statusCode'])
        json_dict_response = json.loads(result['body'])
        self.assertDictEqual({'errors': [{'key_path': 'query_params', 'message': 'Please provide auth_id in query_params'}]}, json_dict_response)

    def test_requirements_decorator_works_and_passes_proper_headers(self):
        dynamic_event = self.mock_request.get_dynamic_event(
            headers={'content-type': 'application/json', 'correlation-id': 'abc-123'},
            path='unit-test/v1/nested/reqs',
            proxy='nested/reqs',
            method='delete'
        )
        router = Router(
            routing_mode='directory',
            base_path=self.base_path,
            handler_path=self.handler_path
        )
        result = router.route(dynamic_event, None)
        self.assertEqual(200, result['statusCode'])

    def test_requirements_decorator_works_and_fails_improper_headers_missing_required(self):
        dynamic_event = self.mock_request.get_dynamic_event(
            headers={'correlation-id': 'abc-123'},
            path='unit-test/v1/nested/reqs',
            proxy='nested/reqs',
            method='delete'
        )
        router = Router(
            routing_mode='directory',
            base_path=self.base_path,
            handler_path=self.handler_path
        )
        result = router.route(dynamic_event, None)
        json_dict_response = json.loads(result['body'])
        self.assertEqual(400, result['statusCode'])
        self.assertDictEqual({'errors': [{'key_path': 'headers', 'message': 'Please provide content-type in headers'}]}, json_dict_response)

    def test_requirements_decorator_works_and_fails_improper_headers_unknown_header(self):
        dynamic_event = self.mock_request.get_dynamic_event(
            headers={'unknown-id': 'abc-123'},
            path='unit-test/v1/nested/reqs',
            proxy='nested/reqs',
            method='delete'
        )
        router = Router(
            routing_mode='directory',
            base_path=self.base_path,
            handler_path=self.handler_path
        )
        result = router.route(dynamic_event, None)
        json_dict_response = json.loads(result['body'])
        self.assertEqual(400, result['statusCode'])
        self.assertDictEqual({'errors': [{'key_path': 'headers', 'message': 'Please provide content-type in headers'}, {'key_path': 'headers', 'message': 'unknown-id is not an available headers'}]}, json_dict_response)
