import base64
import gzip
import json
import unittest

from acai_aws.apigateway.response import Response


class ResponseTest(unittest.TestCase):

    def setUp(self):
        self.response = Response()

    def test_defaults(self):
        self.assertEqual(False, self.response.has_errors)
        self.assertDictEqual(
            self.response.full,
            {
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': '*'
                },
                'statusCode': 204,
                'isBase64Encoded': False,
                'body': '{}'
            }
        )

    def test_default_headers(self):
        self.assertDictEqual(
            self.response.headers, {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': '*'
            }
        )

    def test_closed_cors_headers(self):
        self.response.cors = False
        self.assertDictEqual(self.response.headers, {})
    
    def test_closed_open_cors_headers(self):
        self.response.open_cors = False
        self.assertDictEqual(self.response.headers, {})
        self.assertFalse(self.response.open_cors)

    def test_header_assignment(self):
        self.response.headers = ('some-key', 'some-value')
        self.assertDictEqual(
            self.response.headers, {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': '*',
                'some-key': 'some-value'
            }
        )

    def test_compress(self):
        self.response.body = {'unit-test': True}
        self.response.compress = True
        apigateway_response = self.response.full.copy()
        decoded = json.loads(gzip.decompress(base64.b64decode(apigateway_response['body'])))
        self.assertEqual(apigateway_response['isBase64Encoded'], True)
        self.assertEqual(apigateway_response['headers']['Content-Encoding'], 'gzip')
        self.assertDictEqual(decoded, {'unit-test': True})

    def test_default_code(self):
        self.response.body = {'key': 'value'}
        self.assertEqual(self.response.code, 200)

    def test_assigned_code(self):
        self.response.code = 201
        self.assertEqual(self.response.code, 201)

    def test_empty_body_default_code(self):
        self.assertEqual(self.response.code, 204)

    def test_error_body_default_code(self):
        self.response.set_error('some-error-key', 'some-error-value')
        self.assertEqual(self.response.code, 400)

    def test_is_json(self):
        self.response.is_json = False
        self.response.body = 'not json'
        self.assertEqual(self.response.body, 'not json')

    def test_set_error(self):
        self.response.set_error('some-error-key', 'some-error-value')
        self.assertEqual(
            self.response.body, '{"errors": [{"key_path": "some-error-key", "message": "some-error-value"}]}'
        )

    def test_has_error(self):
        self.response.set_error('some-error-key', 'some-error-value')
        self.assertEqual(self.response.has_errors, True)

    def test_default_content_type_with_default_is_json(self):
        self.assertEqual('application/json', self.response.content_type)

    def test_default_content_type_with_is_json_false(self):
        self.response.is_json = False
        self.assertEqual('', self.response.content_type)

    def test_default_content_type_set_will_stick(self):
        self.response.content_type = 'application/xml'
        self.assertEqual('application/xml', self.response.content_type)

    def test_default_content_type_follows_headers(self):
        self.response.headers = ('Content-Type', 'text/html')
        self.assertEqual('text/html', self.response.content_type)

    def test_raw(self):
        self.response.body = {'raw': True}
        self.assertDictEqual({'raw': True}, self.response.raw)
