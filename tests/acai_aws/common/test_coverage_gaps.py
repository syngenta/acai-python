import unittest

from pydantic import BaseModel

from acai_aws.apigateway.openapi.generator import OpenAPIGenerator
from acai_aws.apigateway.openapi.handler.importer import HandlerImporter
from acai_aws.apigateway.openapi.handler.module import HandlerModule
from acai_aws.apigateway.request import Request
from acai_aws.common.schema import Schema


class SchemaGapsTest(unittest.TestCase):

    def test_get_body_spec_with_no_required_body_returns_empty_dict(self):
        schema = Schema()
        spec = schema.get_body_spec()
        self.assertEqual(spec, {'additionalProperties': False})


class RequestGapsTest(unittest.TestCase):

    def test_body_parser_exception_falls_back_to_raw_body(self):
        request = Request({
            'body': '<not valid xml',
            'headers': {'content-type': 'application/xml'},
        })
        self.assertEqual(request.body, '<not valid xml')

    def test_path_params_setter_recovers_when_internal_state_is_not_dict(self):
        request = Request({})
        request._Request__path_params = 'corrupted'  # pylint: disable=protected-access
        request.path_params = ('user_id', '42')
        self.assertEqual(request.path_params, {'user_id': '42'})


class OpenAPIGeneratorGapsTest(unittest.TestCase):

    def test_delete_unused_paths_removes_entire_path_when_not_registered(self):
        generator = OpenAPIGenerator('tests/mocks/apigateway/openapi/files/yml')
        self.assertIn('/unit-test/v1/schema', generator.doc['paths'])
        generator.delete_unused_paths()
        self.assertEqual(generator.doc['paths'], {})

    def test_delete_unused_paths_removes_only_unused_methods_within_kept_path(self):
        generator = OpenAPIGenerator('tests/mocks/apigateway/openapi/files/yml')
        generator._OpenAPIGenerator__existing_path_methods = {  # pylint: disable=protected-access
            '/unit-test/v1/schema': ['get'],
        }
        generator.delete_unused_paths()
        schema_path = generator.doc['paths']['/unit-test/v1/schema']
        self.assertIn('get', schema_path)
        self.assertNotIn('post', schema_path)
        self.assertNotIn('patch', schema_path)
        self.assertEqual(generator.doc['paths'], {
            '/unit-test/v1/schema': {'get': schema_path['get']},
        })

    def test_add_path_and_method_sets_security_and_request_and_response_bodies(self):
        importer = HandlerImporter()
        generator = OpenAPIGenerator('tests/mocks_outputs')
        modules = importer.get_modules_from_file_paths(
            ['tests/mocks/apigateway/openapi/coverage_gaps.py'],
            'tests/mocks/apigateway/openapi',
            'acai_aws/unit_test',
        )
        post_module = next(m for m in modules if m.method == 'post')
        generator.add_path_and_method(post_module)
        path = generator.doc['paths'][post_module.route_path]['post']
        self.assertEqual(path['security'], [{'AcaiGenerated': []}])
        self.assertIn('requestBody', path)
        self.assertEqual(
            path['requestBody']['content']['application/json']['schema']['$ref'],
            f'#/components/schemas/{post_module.request_body_schema_name}',
        )
        self.assertIn('responses', path)
        self.assertEqual(
            path['responses']['200']['content']['application/json']['schema']['$ref'],
            f'#/components/schemas/{post_module.response_body_schema_name}',
        )


class HandlerModuleGapsTest(unittest.TestCase):

    def test_request_body_schema_inlines_pydantic_defs(self):
        importer = HandlerImporter()
        modules = importer.get_modules_from_file_paths(
            ['tests/mocks/apigateway/openapi/coverage_gaps.py'],
            'tests/mocks/apigateway/openapi',
            'acai_aws/unit_test',
        )
        post_module = next(m for m in modules if m.method == 'post')
        schema = post_module.request_body_schema
        self.assertNotIn('$defs', schema)
        address_property = schema['properties']['address']
        self.assertEqual(address_property.get('type'), 'object')
        self.assertIn('street', address_property['properties'])
        self.assertIn('city', address_property['properties'])

    def test_schema_body_returns_none_for_non_pydantic_non_dict_schema(self):
        importer = HandlerImporter()
        modules = importer.get_modules_from_file_paths(
            ['tests/mocks/apigateway/openapi/coverage_gaps.py'],
            'tests/mocks/apigateway/openapi',
            'acai_aws/unit_test',
        )
        put_module = next(m for m in modules if m.method == 'put')
        self.assertIsNone(put_module.request_body_schema)


if __name__ == '__main__':
    unittest.main()
