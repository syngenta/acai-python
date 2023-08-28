import unittest

from acai.apigateway.router import Router
from tests.acai.apigateway import mock_data
from tests.acai.apigateway import mock_before_all


class ApiGatewayRouterTest(unittest.TestCase):

    def test_router_route(self):
        router = Router(
            base_path='unit-tests/syngenta_digital_alc',
            handler_path='tests.syngenta_digital_alc.apigateway',
            schema_path='tests/openapi.yml',
            event=mock_data.apigateway_route(),
            context=None
        )
        result = router.route()
        self.assertEqual(result['statusCode'], 200)

    def test_router_route_fail(self):
        router = Router(
            base_path='unit-tests/syngenta_digital_alc',
            handler_path='tests.syngenta_digital_alc.apigateway',
            schema_path='tests/openapi.yml',
            event=mock_data.apigateway_route('-fail'),
            context=None
        )
        result = router.route()
        self.assertEqual(result['statusCode'], 404)

    def test_router_before_all_pass(self):
        router = Router(
            base_path='unit-tests/syngenta_digital_alc',
            handler_path='tests.syngenta_digital_alc.apigateway',
            schema_path='tests/openapi.yml',
            event=mock_data.apigateway_route(),
            context=None,
            before_all=mock_before_all.run_pass
        )
        result = router.route()
        self.assertEqual(result['statusCode'], 200)

    def test_router_before_all_pass(self):
        router = Router(
            base_path='unit-tests/syngenta_digital_alc',
            handler_path='tests.syngenta_digital_alc.apigateway',
            schema_path='tests/openapi.yml',
            event=mock_data.apigateway_route(),
            context=None,
            before_all=mock_before_all.run_fail
        )
        result = router.route()
        self.assertEqual(result['statusCode'], 401)
