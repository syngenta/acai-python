import json
import unittest

from acai_aws.apigateway.request_client import RequestClient
from tests.acai_aws.apigateway import mock_data

class ApiGatewayRequestClientTest(unittest.TestCase):

    def setUp(self):
        self.RequestClient = RequestClient(mock_data.apigateway_event(), None)
        self.RequestClientGraphQL = RequestClient(mock_data.apigateway_event_graphql(), None)
        self.RequestClientGraphQLEncoded = RequestClient(mock_data.apigateway_event_graphql(True), None)
        self.RequestClientFormEncoded = RequestClient(mock_data.apigateway_event_form_encoded(), None)

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

    def test_json(self):
        self.assertDictEqual(
            self.RequestClient.json,
            {'body_key':'body_value'}
        )

    def test_graphql(self):
        self.assertDictEqual(
            self.RequestClientGraphQL.graphql,
            json.loads(mock_data.apigateway_event_graphql().get('body'))
        )

    def test_graphql_encoded(self):
        self.assertDictEqual(
            self.RequestClientGraphQLEncoded.graphql,
            json.loads(mock_data.apigateway_event_graphql().get('body'))
        )

    def test_form_encoded(self):
        self.assertDictEqual(
            self.RequestClientFormEncoded.form_encoded,
            {
                'tracking_code': '4081141452',
                'status': 'Complete',
                'cpu_hours': '0.006002831527777777',
                'result_url': 'https://s3.amazonaws.com/fielddata.onsiteag.com/20210506/6499361e-1d72-4fbf-86be-663edc56f840/OnsiteProcessed_20210506_201030.zip?AWSAccessKeyId=AKIA3TR2EEYUQT5E23PG&Expires=1622949031&Signature=ck8zjmWbMweHVIit0j9e%2BeGsGQw%3D'
            }
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
