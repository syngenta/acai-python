import unittest

from acai_aws.apigateway.router import Router
from tests.acai_aws.apigateway import mock_data
from tests.acai_aws.apigateway import mock_before_all


class ApiGatewayRouterTest(unittest.TestCase):

    def test_router_route(self):
        router = Router(
            base_path='unit-tests/acai_aws',
            handler_path='tests.acai_aws.apigateway',
            schema_path='tests/openapi.yml',
            event=mock_data.apigateway_route(),
            context=None
        )
        result = router.route()
        self.assertEqual(result['statusCode'], 200)

    def test_router_route_fail(self):
        router = Router(
            base_path='unit-tests/acai_aws',
            handler_path='tests.acai_aws.apigateway',
            schema_path='tests/openapi.yml',
            event=mock_data.apigateway_route('-fail'),
            context=None
        )
        result = router.route()
        self.assertEqual(result['statusCode'], 404)

    def test_router_before_all_pass(self):
        router = Router(
            base_path='unit-tests/acai_aws',
            handler_path='tests.acai_aws.apigateway',
            schema_path='tests/openapi.yml',
            event=mock_data.apigateway_route(),
            context=None,
            before_all=mock_before_all.run_pass
        )
        result = router.route()
        self.assertEqual(result['statusCode'], 200)

    def test_router_before_all_fail(self):
        router = Router(
            base_path='unit-tests/acai_aws',
            handler_path='tests.acai_aws.apigateway',
            schema_path='tests/openapi.yml',
            event=mock_data.apigateway_route(),
            context=None,
            before_all=mock_before_all.run_fail
        )
        result = router.route()
        self.assertEqual(result['statusCode'], 401)
