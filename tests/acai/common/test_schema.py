import unittest

from openapi_core import Spec

from acai.common.schema import Schema


class SchemaTest(unittest.TestCase):
    schema_path = 'tests/mocks/openapi.yml'
    schema_dict = {
        'type': 'object',
        'required': ['id', 'body'],
        'additionalProperties': False,
        'properties': {
            'id': {
                'type': 'string'
            },
            'body': {
                'type': 'object'
            },
            'dict': {
                'type': 'boolean'
            }
        }
    }
    expect_dict_from_path = {
        'type': 'object',
        'required': ['id', 'body'],
        'additionalProperties': False,
        'properties': {
            'id': {
                'type': 'string'
            },
            'body': {
                'type': 'object'
            },
            'file': {
                'type': 'boolean'
            }
        }
    }
    expect_dict_from_dict = {
        'type': 'object',
        'required': ['id', 'body'],
        'additionalProperties': False,
        'properties': {
            'id': {
                'type': 'string'
            },
            'body': {
                'type': 'object'
            },
            'dict': {
                'type': 'boolean'
            }
        }
    }

    def test_get_schema_from_file(self):
        schema_factory = Schema(schema=self.schema_path)
        schema = schema_factory.get_schema('v1-schema-factory-test')
        self.assertDictEqual(self.expect_dict_from_path, schema)

    def test_get_schema_from_dict(self):
        schema_factory = Schema(schema=self.schema_dict)
        schema = schema_factory.get_schema()
        self.assertDictEqual(self.expect_dict_from_dict, schema)

    def test_get_spec(self):
        schema_factory = Schema(schema=self.schema_path)
        spec = schema_factory.get_spec()
        self.assertTrue(isinstance(spec, Spec))
