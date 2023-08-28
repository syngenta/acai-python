import unittest

from acai_aws.apigateway.request_client import RequestClient
from acai_aws.apigateway.response_client import ResponseClient
from acai_aws.apigateway.request_validator import RequestValidator
from tests.acai_aws.apigateway import mock_data


class RequestValidatorTest(unittest.TestCase):

    OPENAPI = 'tests/openapi.yml'

    def test_validate_headers_pass(self):
        request = RequestClient(mock_data.apigateway_event(), None)
        response = ResponseClient()
        validator = RequestValidator(request, response, self.OPENAPI)
        validator._required_fields(['test-key'], {'test-key': '123456'}, 'headers')
        self.assertFalse(response.has_errors)

    def test_validate_headers_fail(self):
        request = RequestClient(mock_data.apigateway_event(), None)
        response = ResponseClient()
        validator = RequestValidator(request, response, self.OPENAPI)
        validator._required_fields(['test-key'], {'test-key-fail': '123456'}, 'headers')
        self.assertTrue(response.has_errors)

    def test_validate_headers_fail_no_keys(self):
        request = RequestClient(mock_data.apigateway_event(), None)
        response = ResponseClient()
        validator = RequestValidator(request, response, self.OPENAPI)
        validator._required_fields(['test-key'], None, 'params')
        self.assertTrue(response.has_errors)

    def test_validate_path_params_pass(self):
        request = RequestClient(mock_data.apigateway_event(), None)
        response = ResponseClient()
        validator = RequestValidator(request, response, self.OPENAPI)
        validator._required_fields(['test_path'], {'test_path': 'test_value'}, 'path parameters')
        self.assertFalse(response.has_errors)

    def test_validate_path_params_fail(self):
        request = RequestClient(mock_data.apigateway_event(), None)
        response = ResponseClient()
        validator = RequestValidator(request, response, self.OPENAPI)
        validator._required_fields(['test_path'], {'test_path_fail': 'test_value'}, 'path parameters')
        self.assertTrue(response.has_errors)

    def test_validate_params_pass(self):
        request = RequestClient(mock_data.apigateway_event(), None)
        response = ResponseClient()
        validator = RequestValidator(request, response, self.OPENAPI)
        validator._available_fields(['test_path', 'test_path_1'], {'test_path': 'test_value'}, 'params')
        self.assertFalse(response.has_errors)

    def test_validate_params_fail(self):
        request = RequestClient(mock_data.apigateway_event(), None)
        response = ResponseClient()
        validator = RequestValidator(request, response, self.OPENAPI)
        validator._available_fields(['test_path'], {'test_path_fail': 'test_value'}, 'params')
        self.assertTrue(response.has_errors)

    def test_get_schema(self):
        request = RequestClient(mock_data.apigateway_event(), None)
        response = ResponseClient()
        validator = RequestValidator(request, response, self.OPENAPI)
        schema = validator._get_combined_schema('v1-test-request')
        self.assertDictEqual(schema, mock_data.request_schema())

    def test_check_body_for_errors_fail(self):
        request = RequestClient(mock_data.apigateway_event(), None)
        response = ResponseClient()
        validator = RequestValidator(request, response, self.OPENAPI)
        validator._check_body_for_errors('v1-test-request', mock_data.bad_request())
        self.assertTrue(response.has_errors)

    def test_check_body_for_errors_pass(self):
        request = RequestClient(mock_data.apigateway_event(), None)
        response = ResponseClient()
        validator = RequestValidator(request, response, self.OPENAPI)
        validator._check_body_for_errors('v1-test-request', mock_data.valid_request())
        self.assertFalse(response.has_errors)
