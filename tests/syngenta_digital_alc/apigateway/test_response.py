import unittest

from syngenta_digital_alc.apigateway.response_client import ResponseClient


class ReponseTest(unittest.TestCase):

    def test_defaults(self):
        response = ResponseClient()
        self.assertEqual(False, response.has_errors);
        self.assertDictEqual(response.response,
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

    def test_base64_encoded(self):
        response = ResponseClient()
        response.base64_encoded = True
        self.assertEqual(True, response.base64_encoded);
        self.assertDictEqual(response.response,
            {
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': '*'
                },
                'statusCode': 204,
                'isBase64Encoded': True,
                'body': '{}'
            }
        )
