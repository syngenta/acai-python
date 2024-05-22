import importlib.util
import unittest

from acai_aws.apigateway.openapi.handler.module import HandlerModule


class HandlerModuleTest(unittest.TestCase):

    def setUp(self):
        file_path = 'tests/mocks/apigateway/openapi/basic.py'
        import_path = 'tests.mocks.apigateway.openapi.basic'
        spec = importlib.util.spec_from_file_location(import_path, file_path)
        handler_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(handler_module)
        self.module = HandlerModule('tests/mocks/apigateway/openapi', file_path, handler_module, 'post', 'acai_aws/example')

    def test_file_path(self):
        assert self.module.file_path == 'tests/mocks/apigateway/openapi/basic.py'

    def test_module(self):
        assert len(dir(self.module.module)) == 12

    def test_method(self):
        assert self.module.method == 'post'

    def test_operation_id(self):
        assert self.module.operation_id == 'PostAcaiAwsExampleBasicAcaiGenerated'

    def test_route_path(self):
        assert self.module.route_path == '/acai_aws/example/basic'

    def test_deprecated(self):
        assert self.module.deprecated == False

    def test_summary(self):
        assert self.module.summary is None

    def test_tags(self):
        self.assertListEqual(['acai_aws-example'], self.module.tags)

    def test_requires_auth(self):
        assert self.module.requires_auth is None

    def test_required_headers(self):
        self.assertListEqual([], self.module.required_headers)

    def test_available_headers(self):
        self.assertListEqual([], self.module.available_headers)

    def test_required_query(self):
        self.assertListEqual([], self.module.required_query)

    def test_available_query(self):
        self.assertListEqual([], self.module.available_query)

    def test_required_path_params(self):
        self.assertListEqual([], self.module.required_path_params)

    def test_required_path_params(self):
        assert self.module.request_body_schema_name == 'post-acai-aws-example-basic-request-body'

    def test_response_body_schema_name(self):
        assert self.module.response_body_schema_name == 'post-acai-aws-example-basic-response-body'

    def test_request_body_schema(self):
        expected = {
            'title': 'UserRequest',
            'type': 'object',
            'required': ['id', 'email', 'active', 'favorites', 'notification_config'],
            'properties': {
                'id': {
                    'exclusiveMinimum': 0,
                    'title': 'Id',
                    'type': 'integer'
                },
                'email': {
                    'title': 'Email',
                    'type': 'string'
                },
                'active': {
                    'title': 'Active',
                    'type': 'boolean'
                },
                'favorites': {
                    'items': {
                        'type': 'string'
                    },
                    'title': 'Favorites',
                    'type': 'array'
                },
                'notification_config': {
                    'additionalProperties': {
                        'type': 'boolean'},
                    'title': 'Notification Config',
                    'type': 'object'
                }
            }
        }
        self.assertDictEqual(expected, self.module.request_body_schema)

    def test_request_body_schema(self):
        assert self.module.response_body_schema is None
