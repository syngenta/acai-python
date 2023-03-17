import unittest

from acai.apigateway.request import Request
from acai.apigateway.response import Response
from acai.common.validator import Validator

from tests.mocks import mock_request


class ValidatorTest(unittest.TestCase):

    def setUp(self):
        self.validator = Validator()

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

