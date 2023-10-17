import time
import os
from unittest import TestCase, mock

from acai_aws.apigateway.router import Router

from tests.mocks.apigateway import mock_middleware, mock_request


@mock.patch.dict(os.environ, {'LOG_FORMAT': 'INLINE'})
class RouterTimeoutTest(TestCase):
    maxDiff = None
    base_path = 'unit-test/v1'
    handler_path = 'tests/mocks/apigateway/router/directory_handlers'
    schema_path = 'tests/mocks/apigateway/openapi.yml'
    mock_request = mock_request

    def test_global_timeout_works(self):
        dynamic_event = self.mock_request.get_dynamic_event(
            path='unit-test/v1/timeout',
            method='get'
        )
        router = Router(
            base_path=self.base_path,
            handlers=self.handler_path,
            schema=self.schema_path,
            timeout=1
        )
        response = router.route(dynamic_event, None)
        self.assertEqual(408, response['statusCode'])
        
    def test_local_timeout_works(self):
        dynamic_event = self.mock_request.get_dynamic_event(
            path='unit-test/v1/timeout',
            method='get'
        )
        router = Router(
            base_path=self.base_path,
            handlers=self.handler_path,
            schema=self.schema_path
        )
        response = router.route(dynamic_event, None)
        self.assertEqual(408, response['statusCode'])
    
    def test_global_timeout_with_middleware_works(self):
        dynamic_event = self.mock_request.get_dynamic_event(
            path='unit-test/v1/timeout',
            method='post'
        )
        router = Router(
            base_path=self.base_path,
            handlers=self.handler_path,
            schema=self.schema_path,
            timeout=1,
            on_timeout=mock_middleware.mock_on_timeout
        )
        response = router.route(dynamic_event, None)
        self.assertEqual(408, response['statusCode'])
        self.assertTrue(mock_middleware.mock_on_timeout.has_been_called)
    
    def test_local_timeout_with_middleware_works(self):
        dynamic_event = self.mock_request.get_dynamic_event(
            path='unit-test/v1/timeout',
            method='get'
        )
        router = Router(
            base_path=self.base_path,
            handlers=self.handler_path,
            schema=self.schema_path,
            on_timeout=mock_middleware.mock_on_timeout
        )
        response = router.route(dynamic_event, None)
        self.assertEqual(408, response['statusCode'])
        self.assertTrue(mock_middleware.mock_on_timeout.has_been_called)
        
