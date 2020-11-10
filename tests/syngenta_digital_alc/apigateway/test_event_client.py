import unittest

from syngenta_digital_alc.apigateway.request_client import RequestClient
from tests.syngenta_digital_alc.apigateway import mock_data

class ApiGatewayRequestClientTest(unittest.TestCase):

    def setUp(self):
        self.RequestClient = RequestClient(mock_data.apigateway_event())

    def test_request_http_method(self):
        self.assertEqual(self.RequestClient.method, 'GET')

    def test_request_resource(self):
        self.assertEqual(self.RequestClient.resource, '/{proxy+}')

    def test_request_headers(self):
        self.assertDictEqual(
            self.RequestClient.headers,
            {'x-api-key': 'SOME-KEY'}
        )

    def test_request_authorizer(self):
        self.assertDictEqual(
            self.RequestClient.authorizer,
            {
                'x-authorizer-key': 'SOME KEY',
                'principalId':'9de3f415a97e410386dbef146e88744e',
                'integrationLatency':572,
            }
        )

    def test_request_query_string_parameters(self):
        self.assertDictEqual(
            self.RequestClient.params,
            { "name": "me" }
        )
    def test_path_paramters(self):
        self.assertDictEqual(
            self.RequestClient.path_parameters,
            { "proxy": "hello" }
        )

    def test_body(self):
        self.assertDictEqual(
            self.RequestClient.body,
            {'body_key':'body_value'}
        )

    def test_full_request(self):
        self.assertDictEqual(
            self.RequestClient.request,
            {
                'http_method': 'GET',
                'resource': '/{proxy+}',
                'headers': {'x-api-key': 'SOME-KEY'},
                'authorizer': {
                    'x-authorizer-key': 'SOME KEY',
                    'principalId': '9de3f415a97e410386dbef146e88744e',
                    'integrationLatency': 572
                },
                'params': {'name': 'me'},
                'path_parameters': {'proxy': 'hello'},
                'body': {'body_key': 'body_value'}
            }
        )
