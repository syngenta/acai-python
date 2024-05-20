import unittest
import yaml

from acai_aws.apigateway.openapi.handler.importer import HandlerImporter
from acai_aws.apigateway.openapi.generator import OpenAPIGenerator


class OpenAPIGeneratorTest(unittest.TestCase):

    def setUp(self):
        self.non_existing_expected = {
            'openapi': '3.1.0', 
            'info': {'version': '1.0.0', 'title': 'Acai Generator', 'license': {'name': 'MIT'}}, 
            'tags': [{'name': 'acai_aws-unit_test'}], 
            'servers': [], 
            'paths': {
                '/acai_aws/unit_test/basic': {
                    'get': {
                        'tags': ['acai_aws-unit_test'], 
                        'operationId': 'GetAcaiAwsUnitTestBasicAcaiGenerated', 
                        'deprecated': False, 
                        'parameters': [
                            {'in': 'query', 'name': 'basic_id', 'required': True, 'schema': {'type': 'string'}}, 
                            {'in': 'query', 'name': 'first', 'required': False, 'schema': {'type': 'string'}}, 
                            {'in': 'query', 'name': 'last', 'required': False, 'schema': {'type': 'string'}}
                        ]
                    }
                }
            }, 
            'components': {
                'securitySchemes': {'AcaiGenerated': {'type': 'apiKey', 'in': 'header', 'name': 'CHANGE-ME'}}, 
                'schemas': {}
            }
        }  
        with open('tests/mocks/apigateway/openapi.yml', encoding='utf-8') as schema_file:
            self.existing_expected = yaml.load(schema_file, Loader=yaml.FullLoader)
           
    def test_add_path_and_method_existing_file(self):
        generator = OpenAPIGenerator('tests/mocks/apigateway')
        self.assertDictEqual(self.existing_expected, generator.doc)
    
    def test_add_path_and_method_non_existing_file(self):
        importer = HandlerImporter()
        generator = OpenAPIGenerator('tests/mocks_outputs')
        module = importer.get_modules_from_file_paths(['tests/mocks/apigateway/openapi/basic.py'], 'tests/mocks/apigateway/openapi', 'acai_aws/unit_test')[0]
        generator.add_path_and_method(module)
        self.assertDictEqual(self.non_existing_expected, generator.doc)
    
        
