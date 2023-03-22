import unittest

from acai.apigateway.request import Request
from acai.apigateway.openapi.request import OpenAPIRequest

from tests.mocks import mock_request


class RequestTest(unittest.TestCase):
    aws_example = mock_request.get_aws_example()

    def test_host_url(self):
        request = Request(self.aws_example)
        openapi_request = OpenAPIRequest(request)
        self.assertEqual(openapi_request.host_url, 'http://70ixmpl4fl.execute-api.us-east-2.amazonaws.com')

    def test_path(self):
        request = Request(self.aws_example)
        openapi_request = OpenAPIRequest(request)
        self.assertEqual(openapi_request.path, '/')

    def test_method(self):
        request = Request(self.aws_example)
        openapi_request = OpenAPIRequest(request)
        self.assertEqual(openapi_request.method, 'get')

    def test_body(self):
        request = Request(self.aws_example)
        openapi_request = OpenAPIRequest(request)
        self.assertEqual(openapi_request.body, '{"body_key": "body_value"}')

    def test_mimetype(self):
        request = Request(self.aws_example)
        openapi_request = OpenAPIRequest(request)
        self.assertEqual(openapi_request.mimetype, '')
