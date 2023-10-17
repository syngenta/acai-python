import json
import unittest
import urllib

import xmltodict

from acai_aws.apigateway.request import Request
from tests.mocks.apigateway import mock_request


class RequestTest(unittest.TestCase):
    websocket_aws_example = mock_request.get_aws_websocket_example()
    aws_example = mock_request.get_aws_example()
    basic_request = mock_request.get_basic()
    basic_offline = mock_request.get_basic_offline()
    basic_form = mock_request.get_basic_form()
    basic_xml = mock_request.get_basic_xml()
    basic_raw = mock_request.get_basic_raw()
    basic_graphql = mock_request.get_basic_graphql()
    basic_graphql_variables = mock_request.basic_graphql_variables()
    missing_inputs = mock_request.get_request_with_missing_fields()

    def test_method(self):
        request = Request(self.basic_request)
        self.assertEqual(request.method, self.basic_request['httpMethod'].lower())

    def test_cookies(self):
        request = Request(self.aws_example)
        self.assertEqual(request.cookies, self.aws_example['headers']['cookie'])

    def test_websocket_cookies(self):
        request = Request(self.websocket_aws_example)
        self.assertEqual(request.cookies, ';'.join(self.websocket_aws_example.get('cookies', [])))

    def test_content_type(self):
        request = Request(self.basic_request)
        self.assertEqual(request.content_type, self.basic_request['headers']['content-type'])

    def test_protocol(self):
        request = Request(self.aws_example)
        self.assertEqual(request.protocol, 'http')

    def test_websocket_protocol(self):
        request = Request(self.websocket_aws_example)
        self.assertEqual(request.protocol, 'http')

    def test_host_url(self):
        request = Request(self.aws_example)
        self.assertEqual(request.host_url, 'http://70ixmpl4fl.execute-api.us-east-2.amazonaws.com')

    def test_domain(self):
        request = Request(self.aws_example)
        self.assertEqual(request.domain, '70ixmpl4fl.execute-api.us-east-2.amazonaws.com')

    def test_stage(self):
        request = Request(self.aws_example)
        self.assertEqual(request.stage, 'Prod')

    def test_resource(self):
        request = Request(self.basic_request)
        self.assertEqual(request.resource, self.basic_request['resource'])

    def test_path(self):
        request = Request(self.basic_request)
        self.assertEqual(request.path, self.basic_request['path'])

    def test_route_default(self):
        request = Request(self.basic_request)
        self.assertEqual(request.route, f'/{self.basic_request["path"]}')

    def test_route_mutated(self):
        mutated = '/unit-test/v1/mutated'
        request = Request(self.basic_request)
        request.route = mutated
        self.assertEqual(request.route, mutated)

    def test_authorizer(self):
        request = Request(self.basic_request)
        self.assertDictEqual(request.authorizer, self.basic_request['requestContext']['authorizer'])

    def test_authorizer_offline(self):
        request = Request(self.basic_offline)
        self.assertDictEqual(request.authorizer, self.basic_offline['headers'])

    def test_headers(self):
        request = Request(self.basic_request)
        self.assertDictEqual(request.headers, self.basic_request['headers'])

    def test_body_json(self):
        request = Request(self.basic_request)
        self.assertDictEqual(request.body, json.loads(self.basic_request['body']))

    def test_json(self):
        request = Request(self.basic_request)
        self.assertDictEqual(request.json, json.loads(self.basic_request['body']))

    def test_body_form(self):
        request = Request(self.basic_form)
        self.assertDictEqual(request.body, dict(urllib.parse.parse_qsl(self.basic_form['body'])))

    def test_form(self):
        request = Request(self.basic_form)
        self.assertDictEqual(request.form, dict(urllib.parse.parse_qsl(self.basic_form['body'])))

    def test_body_xml(self):
        request = Request(self.basic_xml)
        self.assertDictEqual(request.body, xmltodict.parse(self.basic_xml['body']))

    def test_xml(self):
        request = Request(self.basic_xml)
        self.assertDictEqual(request.xml, xmltodict.parse(self.basic_xml['body']))

    def test_body_raw(self):
        request = Request(self.basic_raw)
        self.assertEqual(request.body, self.basic_raw['body'])

    def test_raw(self):
        request = Request(self.basic_raw)
        self.assertEqual(request.raw, self.basic_raw['body'])

    def test_body_graphql(self):
        request = Request(self.basic_graphql)
        self.assertEqual(request.body, self.basic_graphql['body'])

    def test_graphql(self):
        request = Request(self.basic_graphql)
        self.assertEqual(request.graphql, self.basic_graphql['body'])

    def test_graphql_base64(self):
        base64_graphql = self.basic_graphql.copy()
        base64_graphql['body'] = 'e3BsYXllcnN7bmFtZX19'  # used online tool to generate this
        request = Request(base64_graphql)
        self.assertEqual(request.graphql, self.basic_graphql['body'])

    def test_graphql_bad_base64(self):
        bad_base64_graphql = self.basic_graphql.copy()
        bad_base64_graphql['body'] = 1234
        request = Request(bad_base64_graphql)
        self.assertEqual(request.graphql, bad_base64_graphql['body'])

    def test_graphql_with_variables(self):
        request = Request(self.basic_graphql_variables)
        self.assertDictEqual(request.graphql, json.loads(self.basic_graphql_variables['body']))

    def test_query_params(self):
        request = Request(self.basic_request)
        self.assertDictEqual(request.query_params, self.basic_request['queryStringParameters'])

    def test_path_params(self):
        request = Request(self.basic_request)
        self.assertDictEqual(request.path_params, self.basic_request['pathParameters'])

    def test_path_params_setter(self):
        request = Request(self.basic_request)
        request.clear_path_params()
        request.path_params = ('hello', 'world')
        self.assertDictEqual(request.path_params, {'hello': 'world'})

    def test_path_params_clear(self):
        request = Request(self.basic_request)
        request.clear_path_params()
        self.assertDictEqual(request.path_params, {})

    def test_params(self):
        request = Request(self.basic_request)
        result = {'query': self.basic_request['queryStringParameters'], 'path': self.basic_request['pathParameters']}
        self.assertDictEqual(request.params, result)

    def test_context_default(self):
        request = Request(self.basic_request)
        self.assertDictEqual(request.context, {})

    def test_context_mutatable(self):
        context = {'hello': 'context'}
        request = Request(self.basic_request)
        request.context = context
        self.assertDictEqual(request.context, context)

    def test_event(self):
        request = Request(self.basic_request)
        self.assertDictEqual(
            request.event, {
                'headers': {
                    'x-api-key': 'SOME-KEY',
                    'content-type': 'application/json'
                },
                'requestContext': {
                    'resourceId': 't89kib',
                    'authorizer': {
                        'x-authorizer-key': 'SOME KEY',
                        'principalId': '9de3f415a97e410386dbef146e88744e',
                        'integrationLatency': 572
                    }
                },
                'path': 'unit-test/v1/basic',
                'pathParameters': {'proxy': 'hello'},
                'resource': '/{proxy+}',
                'httpMethod': 'GET',
                'queryStringParameters': {'name': 'me'},
                'body': '{"body_key": "body_value"}'
            }
        )

    def test_request(self):
        request = Request(self.basic_request)
        self.assertDictEqual(
            request.full, {
                'method': 'get',
                'resource': '/{proxy+}',
                'headers': {
                    'x-api-key': 'SOME-KEY',
                    'content-type': 'application/json'
                },
                'authorizer': {
                    'x-authorizer-key': 'SOME KEY',
                    'principalId': '9de3f415a97e410386dbef146e88744e',
                    'integrationLatency': 572
                },
                'params': {'query': {'name': 'me'}, 'path': {'proxy': 'hello'}},
                'body': {'body_key': 'body_value'},
                'context': {}
            }
        )

    def test_str(self):
        request = Request(self.basic_request)
        self.assertEqual(
            str(request),
            '{"method": "get", "resource": "/{proxy+}", "headers": {"x-api-key": "SOME-KEY", '
            '"content-type": "application/json"}, "authorizer": {"x-authorizer-key": "SOME KEY", '
            '"principalId": "9de3f415a97e410386dbef146e88744e", "integrationLatency": 572}, "params": {'
            '"query": {"name": "me"}, "path": {"proxy": "hello"}}, "body": {"body_key": "body_value"}, '
            '"context": {}}'
        )
    
    def test_defaults(self):
        request = Request(self.missing_inputs)
        self.assertEqual(request.method, '')
        self.assertEqual(request.resource, '')
        self.assertEqual(request.path, '')
        self.assertEqual(request.query_params, {})
    
    def test_timeout(self):
        request = Request(self.basic_request, None, 30)
        self.assertEqual(request.timeout, 30)
