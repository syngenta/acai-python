import unittest

from acai_aws.apigateway.request import Request
from acai_aws.apigateway.response import Response
from acai_aws.common.validator import Validator

from tests.mocks.apigateway import mock_request
from tests.mocks.common.mock_pydantic_class import UserRequest


class ValidatorTest(unittest.TestCase):
    schema_path = 'tests/mocks/common/openapi.yml'

    def setUp(self):
        self.validator = Validator(schema=self.schema_path)

    def test_empty_validation(self):
        request = Request(mock_request.get_basic_for_validation())
        response = Response()
        requirements = {}
        self.validator.validate_request(request, response, requirements)
        self.assertFalse(response.has_errors)

    def test_required_headers_pass(self):
        request = Request(mock_request.get_basic_for_validation())
        response = Response()
        requirements = {
            'required_headers': ['content-type']
        }
        self.validator.validate_request(request, response, requirements)
        self.assertFalse(response.has_errors)

    def test_required_headers_fails(self):
        request = Request(mock_request.get_basic_for_validation())
        response = Response()
        requirements = {
            'required_headers': ['content-type-fails']
        }
        self.validator.validate_request(request, response, requirements)
        self.assertTrue(response.has_errors)
        self.assertEqual('{"errors": [{"key_path": "headers", "message": "Please provide content-type-fails in headers"}]}', response.full['body'])

    def test_available_headers_pass(self):
        request = Request(mock_request.get_basic_for_validation())
        response = Response()
        requirements = {
            'available_headers': ['content-type']
        }
        self.validator.validate_request(request, response, requirements)
        self.assertFalse(response.has_errors)

    def test_available_headers_fails(self):
        request = Request(mock_request.get_basic_for_validation())
        response = Response()
        requirements = {
            'available_headers': ['content-type-fail']
        }
        self.validator.validate_request(request, response, requirements)
        self.assertTrue(response.has_errors)
        self.assertEqual('{"errors": [{"key_path": "headers", "message": "content-type is not an available headers"}]}', response.full['body'])

    def test_required_query_pass(self):
        request = Request(mock_request.get_basic_for_validation())
        response = Response()
        requirements = {
            'required_query': ['email']
        }
        self.validator.validate_request(request, response, requirements)
        self.assertFalse(response.has_errors)

    def test_required_query_fail(self):
        request = Request(mock_request.get_basic_for_validation())
        response = Response()
        requirements = {
            'required_query': ['email', 'other']
        }
        self.validator.validate_request(request, response, requirements)
        self.assertTrue(response.has_errors)
        self.assertEqual('{"errors": [{"key_path": "query_params", "message": "Please provide other in query_params"}]}', response.full['body'])

    def test_available_query_pass(self):
        request = Request(mock_request.get_basic_for_validation())
        response = Response()
        requirements = {
            'available_query': ['email', 'other']
        }
        self.validator.validate_request(request, response, requirements)
        self.assertFalse(response.has_errors)

    def test_available_query_fail(self):
        request = Request(mock_request.get_basic_for_validation())
        response = Response()
        requirements = {
            'available_query': ['other']
        }
        self.validator.validate_request(request, response, requirements)
        self.assertTrue(response.has_errors)
        self.assertEqual('{"errors": [{"key_path": "query_params", "message": "email is not an available query_params"}]}', response.full['body'])

    def test_required_body_pass(self):
        request = Request(mock_request.get_basic_passing_for_required_body_validation())
        response = Response()
        requirements = {
            'required_body': 'v1-required-body-test'
        }
        self.validator.validate_request(request, response, requirements)
        self.assertFalse(response.has_errors)

    def test_required_body_fail(self):
        request = Request(mock_request.get_basic_failing_for_required_body_validation())
        response = Response()
        requirements = {
            'required_body': 'v1-required-body-test'
        }
        self.validator.validate_request(request, response, requirements)
        self.assertTrue(response.has_errors)
        self.assertEqual('{"errors": [{"key_path": "root", "message": "\'id\' is a required property"}]}', response.body)

    def test_validate_request_with_openapi_passes(self):
        request = Request(mock_request.get_auto_validated_data())
        response = Response()
        self.validator.validate_request_with_openapi(request, response)
    
    def test_required_pydantic_body_pass(self):
        request = Request(mock_request.get_basic_passing_for_required_body_validation())
        response = Response()
        requirements = {
            'required_body': UserRequest
        }
        self.validator.validate_request(request, response, requirements)
        self.assertFalse(response.has_errors)
    
    def test_required_pydantic_body_fail(self):
        request = Request(mock_request.get_basic_failing_for_required_body_validation())
        response = Response()
        requirements = {
            'required_body': UserRequest
        }
        self.validator.validate_request(request, response, requirements)
        self.assertTrue(response.has_errors)
        self.assertEqual('{"errors": [{"key_path": "id", "message": "Field required"}]}', response.body)
