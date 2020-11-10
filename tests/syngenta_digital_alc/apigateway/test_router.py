import unittest

from syngenta_digital_alc.apigateway.router import Router
from tests.syngenta_digital_alc.apigateway import mock_data

class ApiGatewayRouterTest(unittest.TestCase):

    def test_router_route(self):
        router = Router(
            base_path='unit-tests/syngenta_digital_alc/apigateway',
            handler_path='tests.syngenta_digital_alc.apigateway',
            schema_path='tests/openapi.yml',
            event=mock_data.apigateway_route(),
            context=None
        )
        result = router.route()
        self.assertEqual(result['statusCode'], 200)

    def test_router_route_fail(self):
        router = Router(
            base_path='unit-tests/syngenta_digital_alc/apigateway',
            handler_path='tests.syngenta_digital_alc.apigateway',
            schema_path='tests/openapi.yml',
            event=mock_data.apigateway_route('-fail'),
            context=None
        )
        result = router.route()
        self.assertEqual(result['statusCode'], 404)
