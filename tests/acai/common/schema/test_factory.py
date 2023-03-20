import unittest

from acai.common.schema.factory import SchemaFactory


class SchemaFactoryTest(unittest.TestCase):
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
        schema_factory = SchemaFactory(schema=self.schema_path)
        schema = schema_factory.get_schema('v1-schema-factory-test')
        self.assertDictEqual(self.expect_dict_from_path, schema)

    def test_get_schema_from_dict(self):
        schema_factory = SchemaFactory(schema=self.schema_dict)
        schema = schema_factory.get_schema()
        self.assertDictEqual(self.expect_dict_from_dict, schema)


