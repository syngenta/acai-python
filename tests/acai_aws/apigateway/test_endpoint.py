import unittest

from acai_aws.apigateway.endpoint import Endpoint
from acai_aws.apigateway.resolver.importer import ResolverImporter
from acai_aws.apigateway.request import Request
from acai_aws.apigateway.response import Response


class EndpointTest(unittest.TestCase):
    handler_path = 'tests/mocks/apigateway/endpoint/directory_handlers'

    def test_endpoint_initializes(self):
        importer = ResolverImporter(handlers=self.handler_path, mode='directory')
        file_path = f'{self.handler_path}/basic.py'
        import_path = 'tests.mocks.apigateway.endpoint.directory_handlers.basic'
        endpoint_module = importer.import_module_from_file(file_path, import_path)
        endpoint = Endpoint(endpoint_module, 'post')
        self.assertTrue(isinstance(endpoint, Endpoint))

    def test_endpoint_has_requirements(self):
        importer = ResolverImporter(handlers=self.handler_path, mode='directory')
        file_path = f'{self.handler_path}/basic.py'
        import_path = 'tests.mocks.apigateway.endpoint.directory_handlers.basic'
        endpoint_module = importer.import_module_from_file(file_path, import_path)
        endpoint = Endpoint(endpoint_module, 'post')
        self.assertTrue(endpoint.has_requirements)

    def test_endpoint_has_no_requirements(self):
        importer = ResolverImporter(handlers=self.handler_path, mode='directory')
        file_path = f'{self.handler_path}/basic.py'
        import_path = 'tests.mocks.apigateway.endpoint.directory_handlers.basic'
        endpoint_module = importer.import_module_from_file(file_path, import_path)
        endpoint = Endpoint(endpoint_module, 'patch')
        self.assertFalse(endpoint.has_requirements)

    def test_endpoint_requires_auth(self):
        importer = ResolverImporter(handlers=self.handler_path, mode='directory')
        file_path = f'{self.handler_path}/basic.py'
        import_path = 'tests.mocks.apigateway.endpoint.directory_handlers.basic'
        endpoint_module = importer.import_module_from_file(file_path, import_path)
        endpoint = Endpoint(endpoint_module, 'get')
        self.assertTrue(endpoint.requires_auth)

    def test_endpoint_has_required_response(self):
        importer = ResolverImporter(handlers=self.handler_path, mode='directory')
        file_path = f'{self.handler_path}/basic.py'
        import_path = 'tests.mocks.apigateway.endpoint.directory_handlers.basic'
        endpoint_module = importer.import_module_from_file(file_path, import_path)
        endpoint = Endpoint(endpoint_module, 'search')
        self.assertTrue(endpoint.has_required_response)

    def test_endpoint_has_required_route(self):
        importer = ResolverImporter(handlers=self.handler_path, mode='directory')
        file_path = f'{self.handler_path}/basic.py'
        import_path = 'tests.mocks.apigateway.endpoint.directory_handlers.basic'
        endpoint_module = importer.import_module_from_file(file_path, import_path)
        endpoint = Endpoint(endpoint_module, 'delete')
        self.assertTrue(endpoint.has_required_route)
        self.assertEqual('/some/route/{id}', endpoint.required_route)

    def test_endpoint_supports_custom_requirements(self):
        importer = ResolverImporter(handlers=self.handler_path, mode='directory')
        file_path = f'{self.handler_path}/basic.py'
        import_path = 'tests.mocks.apigateway.endpoint.directory_handlers.basic'
        endpoint_module = importer.import_module_from_file(file_path, import_path)
        endpoint = Endpoint(endpoint_module, 'put')
        self.assertTrue(endpoint.has_requirements)
        self.assertDictEqual({'custom_list': [1, 2, 3], 'custom_dict': {'key': 'value'}, 'custom_simple': 1}, endpoint.requirements)

    def test_endpoint_runs_empty_requirements(self):
        importer = ResolverImporter(handlers=self.handler_path, mode='directory')
        file_path = f'{self.handler_path}/basic.py'
        import_path = 'tests.mocks.apigateway.endpoint.directory_handlers.basic'
        endpoint_module = importer.import_module_from_file(file_path, import_path)
        endpoint = Endpoint(endpoint_module, 'post')
        response = Response()
        request = Request({})
        result = endpoint.run(request, response)
        self.assertEqual('{"endpoint_directory_basic": "post"}', result.full['body'])

    def test_endpoint_runs_no_requirements(self):
        importer = ResolverImporter(handlers=self.handler_path, mode='directory')
        file_path = f'{self.handler_path}/basic.py'
        import_path = 'tests.mocks.apigateway.endpoint.directory_handlers.basic'
        endpoint_module = importer.import_module_from_file(file_path, import_path)
        endpoint = Endpoint(endpoint_module, 'patch')
        response = Response()
        request = Request({})
        result = endpoint.run(request, response)
        self.assertEqual('{"endpoint_directory_basic": "patch"}', result.full['body'])
