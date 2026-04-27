import unittest

from acai_aws.alb.response import Response


class ALBResponseTest(unittest.TestCase):
    maxDiff = None

    def test_response_includes_status_description_on_full(self):
        response = Response()
        response.body = {'ok': True}
        full = response.full
        self.assertEqual('200 OK', full['statusDescription'])
        self.assertEqual(200, full['statusCode'])

    def test_response_status_description_for_known_codes(self):
        response = Response()
        response.code = 404
        response.body = {'errors': [{'key_path': 'route', 'message': 'not found'}]}
        self.assertEqual('404 Not Found', response.full['statusDescription'])

    def test_response_status_description_unknown_code_falls_back_to_ok(self):
        response = Response()
        response.code = 599
        response.body = {'msg': 'weird'}
        self.assertEqual('599 OK', response.full['statusDescription'])

    def test_response_full_includes_alb_required_keys(self):
        response = Response()
        response.body = {'ok': True}
        full = response.full
        self.assertIn('statusCode', full)
        self.assertIn('statusDescription', full)
        self.assertIn('body', full)
        self.assertIn('headers', full)
        self.assertIn('isBase64Encoded', full)


if __name__ == '__main__':
    unittest.main()
