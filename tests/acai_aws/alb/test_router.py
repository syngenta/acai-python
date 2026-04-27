import json
import unittest

from acai_aws.alb.router import Router

from tests.mocks.alb import mock_request


class ALBRouterTest(unittest.TestCase):
    """Smoke tests confirming alb.Router routes ALB events through the apigateway
    Router internals while applying ALB-specific request/response handling."""

    maxDiff = None
    base_path = 'unit-test/v1'
    handler_path = 'tests/mocks/apigateway/router/directory_handlers'

    def test_basic_directory_routing_works(self):
        router = Router(
            base_path=self.base_path,
            handlers=self.handler_path,
        )
        result = router.route(mock_request.get_basic_post(), None)
        self.assertEqual(200, result['statusCode'])
        self.assertEqual('200 OK', result['statusDescription'])
        self.assertFalse(result['isBase64Encoded'])
        self.assertDictEqual(
            {'router_directory_basic': {'body_key': 'body_value'}},
            json.loads(result['body']),
        )

    def test_routing_decodes_base64_body_end_to_end(self):
        router = Router(
            base_path=self.base_path,
            handlers=self.handler_path,
        )
        result = router.route(mock_request.get_basic_post_base64(), None)
        self.assertEqual(200, result['statusCode'])
        self.assertEqual('200 OK', result['statusDescription'])
        self.assertDictEqual(
            {'router_directory_basic': {'body_key': 'body_value'}},
            json.loads(result['body']),
        )

    def test_routing_supports_dynamic_path_parameters(self):
        event = mock_request.get_dynamic_event(
            path='unit-test/v1/user/1',
            method='get',
        )
        router = Router(
            base_path=self.base_path,
            handlers=self.handler_path,
        )
        result = router.route(event, None)
        self.assertEqual(200, result['statusCode'])
        self.assertDictEqual(
            {'directory_user_id': {'user_id': '1'}},
            json.loads(result['body']),
        )

    def test_routing_supports_multiple_dynamic_segments(self):
        event = mock_request.get_dynamic_event(
            path='unit-test/v1/triple/1/2/3',
            method='post',
        )
        router = Router(
            base_path=self.base_path,
            handlers=self.handler_path,
        )
        result = router.route(event, None)
        self.assertEqual(200, result['statusCode'])
        self.assertDictEqual(
            {'directory_triple_coordinates': {'x': '1', 'y': '2', 'z': '3'}},
            json.loads(result['body']),
        )

    def test_unknown_route_returns_404_with_status_description(self):
        event = mock_request.get_dynamic_event(
            path='unit-test/v1/does-not-exist',
            method='get',
        )
        router = Router(
            base_path=self.base_path,
            handlers=self.handler_path,
        )
        result = router.route(event, None)
        self.assertEqual(404, result['statusCode'])
        self.assertEqual('404 Not Found', result['statusDescription'])

    def test_routing_can_opt_out_of_cors(self):
        router = Router(
            base_path=self.base_path,
            handlers=self.handler_path,
            cors=False,
        )
        result = router.route(mock_request.get_basic_post(), None)
        self.assertNotIn('Access-Control-Allow-Origin', result['headers'])


if __name__ == '__main__':
    unittest.main()
