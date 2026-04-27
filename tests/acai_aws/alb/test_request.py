import unittest

from acai_aws.alb.request import Request

from tests.mocks.alb import mock_request


class ALBRequestTest(unittest.TestCase):
    maxDiff = None

    def test_request_reads_alb_event_shape(self):
        request = Request(mock_request.get_basic_post())
        self.assertEqual('post', request.method)
        self.assertEqual('unit-test/v1/basic', request.path)
        self.assertEqual({'name': 'me'}, request.query_params)
        self.assertEqual({'body_key': 'body_value'}, request.body)

    def test_request_decodes_base64_body(self):
        request = Request(mock_request.get_basic_post_base64())
        self.assertEqual({'body_key': 'body_value'}, request.body)

    def test_request_target_group_arn(self):
        request = Request(mock_request.get_basic_post())
        self.assertEqual(
            'arn:aws:elasticloadbalancing:us-east-1:123456789012:targetgroup/acai-tg/50dc6c495c0c9188',
            request.target_group_arn,
        )

    def test_request_target_group_arn_missing_returns_empty(self):
        event = mock_request.get_basic_post()
        event['requestContext'] = {}
        request = Request(event)
        self.assertEqual('', request.target_group_arn)

    def test_request_source_ip_from_xff_header(self):
        request = Request(mock_request.get_basic_post())
        self.assertEqual('203.0.113.42', request.source_ip)

    def test_request_source_ip_missing_returns_empty(self):
        event = mock_request.get_basic_post()
        event['headers'] = {'content-type': 'application/json'}
        request = Request(event)
        self.assertEqual('', request.source_ip)

    def test_request_lowercases_headers(self):
        event = mock_request.get_basic_post()
        event['headers'] = {'X-Custom-Header': 'value', 'Content-Type': 'application/json'}
        request = Request(event)
        self.assertEqual('value', request.headers.get('x-custom-header'))


if __name__ == '__main__':
    unittest.main()
