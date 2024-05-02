import unittest

from pydantic import BaseModel

from acai_aws.common.schema import Schema
from tests.mocks.common.mock_pydantic_class import Request


class SchemaTest(unittest.TestCase):
    maxDiff = None
    schema_path = 'tests/mocks/common/openapi.yml'
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
    expected_dict_from_path = {
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
    expected_dict_from_dict = {
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
    expected_combined_dict = {
        'type': 'object',
        'properties': {
            'test_id': {
                'type': 'string'
            },
            'object_key': {
                'type': 'object',
                'properties': {
                    'string_key': {
                        'type': 'string'
                    }
                }
            },
            'array_number': {
                'type': 'array',
                'items': {
                    'type': 'number'
                }
            },
            'array_objects': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'array_string_key': {
                            'type': 'string'
                        },
                        'array_number_key': {
                            'type': 'number'
                        }
                    }
                }
            },
            'fail_id': {
                'type': 'string'
            }
        },
        'required': ['test_id', 'object_key', 'array_number', 'array_objects'],
        'additionalProperties': False
    }
    expected_route_spec = {
        'tags': [
            'unit-test'
        ],
        'operationId': 'GetSchema',
        'deprecated': False,
        'parameters': [
            {
                'in': 'query',
                'name': 'test_id',
                'required': False,
                'schema': {
                    'type': 'string'
                }
            },
            {
                'in': 'query',
                'name': 'unit_id',
                'required': True,
                'schema': {
                    'type': 'string'
                }
            }
        ],
        'responses': {
            '200': {
                'description': 'valid',
                'content': {
                    'application/json': {
                        'schema': {
                            'type': 'object',
                            'properties': {
                                'page_number': {
                                    'type': 'number'
                                },
                                'data': {
                                    'type': 'object',
                                    'required': [
                                        'id'
                                    ],
                                    'properties': {
                                        'id': {
                                            'type': 'string'
                                        }
                                    }
                                }
                            },
                            'required': [
                                'page_number',
                                'data'
                            ]
                        }
                    }
                }
            }
        }
    }

    def test_get_openapi_spec(self):
        schema_factory = Schema(schema=self.schema_path)
        spec = schema_factory.get_openapi_spec()
        self.assertTrue(isinstance(spec, dict))

    def test_get_body_spec_from_file(self):
        schema = Schema(schema=self.schema_path)
        spec = schema.get_body_spec('v1-schema-factory-test')
        self.assertDictEqual(self.expected_dict_from_path, spec)

    def test_get_combined_body_spec_from_file(self):
        schema = Schema(schema=self.schema_path)
        spec = schema.get_body_spec('v1-test-request')
        self.assertDictEqual(self.expected_combined_dict, spec)

    def test_get_body_spec_from_dict(self):
        schema = Schema(schema=self.schema_dict)
        spec = schema.get_body_spec()
        self.assertDictEqual(self.expected_dict_from_dict, spec)
    
    def test_get_body_spec_from_pydantic_model(self):
        schema = Schema(schema=self.schema_path)
        spec = schema.get_body_spec(Request)
        self.assertTrue(issubclass(spec, BaseModel))

    def test_get_spec_from_route(self):
        schema = Schema(schema=self.schema_path)
        spec = schema.get_route_spec('/unit-test/v1/schema', 'get')
        self.assertDictEqual(self.expected_route_spec, spec)
