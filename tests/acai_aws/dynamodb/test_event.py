import unittest

from acai_aws.dynamodb.event import Event
from acai_aws.dynamodb.record import Record
from acai_aws.common.records.exception import RecordException

from tests.mocks.dynamodb import mock_event
from tests.mocks.dynamodb.mock_data_class import MockDDBDataClass


class DynamoDBEventTest(unittest.TestCase):
    created_event = mock_event.get_created_event()
    updated_event = mock_event.get_updated_event()
    deleted_event = mock_event.get_deleted_event()
    schema_path = 'tests/mocks/dynamodb/openapi.yml'
    expected_body = {
        'example_id': '123456789',
        'note': 'Hosrawguw verrig zogupap ce so fajdis vub mos sif mawpowpug kif kihane.',
        'active': True,
        'personal': {
            'gender': 'male',
            'last_name': 'Mcneil',
            'first_name': 'Mannix'
        },
        'transportation': ['public-transit', 'car-access']
    }

    def test_event_accepts_event(self):
        event = Event(self.created_event)
        self.assertEqual(event.context, None)
        self.assertEqual(event.data_class, None)
        self.assertDictEqual(event.event, self.created_event)
        self.assertEqual(len(event.records), len(self.created_event['Records']))

    def test_event_raw_records(self):
        event = Event(self.created_event)
        self.assertCountEqual(event.raw_records, self.created_event['Records'])

    def test_event_returns_record_event(self):
        event = Event(self.created_event)
        self.assertTrue(isinstance(event.records[0], Record))

    def test_event_returns_data_class(self):
        event = Event(self.created_event)
        event.data_class = MockDDBDataClass
        self.assertTrue(isinstance(event.records[0], MockDDBDataClass))
        self.assertTrue(isinstance(event.records[0].record, Record))

    def test_event_validate_record_body_with_schema_file(self):
        event = Event(self.created_event, schema=self.schema_path, required_body='v1-ddb-body')
        self.assertDictEqual(event.records[0].body, self.expected_body)

    def test_event_validate_filters_out_record_body_with_schema_file(self):
        event = Event(self.created_event, schema=self.schema_path, required_body='v1-ddb-body-wrong')
        self.assertEqual(len(event.records), 0)

    def test_event_validate_raises_exception_record_body_with_schema_file(self):
        try:
            event = Event(self.created_event, schema=self.schema_path, required_body='v1-ddb-body-wrong', raise_body_error=True)
            print(event.records)
            self.assertTrue(False)
        except RecordException as record_error:
            self.assertTrue(isinstance(record_error, RecordException))

    def test_event_validate_record_body_with_schema_dict(self):
        schema = {
            '$id': 'https://example.com/person.schema.json',
            '$schema': 'https://json-schema.org/draft/2020-12/schema',
            'type': 'object',
            'required': [
                'example_id',
                'note',
                'active',
                'personal',
                'transportation'
            ],
            'properties': {
                'example_id': {
                    'type': 'string'
                },
                'note': {
                    'type': 'string'
                },
                'active': {
                    'type': 'boolean'
                },
                'personal': {
                    'type': 'object',
                    'properties': {
                        'gender': {
                            'type': 'string'
                        },
                        'first_name': {
                            'type': 'string'
                        },
                        'last_name': {
                            'type': 'string'
                        }
                    }
                },
                'transportation': {
                    'type': 'array',
                    'items': {
                        'type': 'string'
                    }
                }
            }
        }
        event = Event(self.created_event, schema=self.schema_path, required_body=schema)
        self.assertDictEqual(event.records[0].body, self.expected_body)

    def test_event_validate_raises_error_record_body_with_schema_dict(self):
        schema = {
            '$id': 'https://example.com/person.schema.json',
            '$schema': 'https://json-schema.org/draft/2020-12/schema',
            'type': 'object',
            'required': [
                'example_id',
                'note',
                'active',
                'personal',
                'transportation'
            ],
            'properties': {
                'example_id': {
                    'type': 'string'
                },
                'note': {
                    'type': 'boolean'
                },
                'active': {
                    'type': 'boolean'
                },
                'personal': {
                    'type': 'object',
                    'properties': {
                        'gender': {
                            'type': 'string'
                        },
                        'first_name': {
                            'type': 'string'
                        },
                        'last_name': {
                            'type': 'string'
                        }
                    }
                },
                'transportation': {
                    'type': 'array',
                    'items': {
                        'type': 'string'
                    }
                }
            }
        }
        try:
            event = Event(self.created_event, schema=self.schema_path, required_body=schema, raise_body_error=True)
            print(event.records)
            self.assertTrue(False)
        except RecordException as record_error:
            self.assertTrue(isinstance(record_error, RecordException))

    def test_event_validate_filters_out_record_body_with_schema_dict(self):
        schema = {
            '$id': 'https://example.com/person.schema.json',
            '$schema': 'https://json-schema.org/draft/2020-12/schema',
            'type': 'object',
            'required': [
                'example_id',
                'note',
                'active',
                'personal',
                'transportation'
            ],
            'properties': {
                'example_id': {
                    'type': 'string'
                },
                'note': {
                    'type': 'boolean'
                },
                'active': {
                    'type': 'boolean'
                },
                'personal': {
                    'type': 'object',
                    'properties': {
                        'gender': {
                            'type': 'string'
                        },
                        'first_name': {
                            'type': 'string'
                        },
                        'last_name': {
                            'type': 'string'
                        }
                    }
                },
                'transportation': {
                    'type': 'array',
                    'items': {
                        'type': 'string'
                    }
                }
            }
        }
        event = Event(self.created_event, schema=self.schema_path, required_body=schema)
        self.assertEqual(len(event.records), 0)

    def test_event_print(self):
        event = Event(self.created_event)
        try:
            print(event)
            self.assertTrue(True)
        except Exception as error:
            print(error)
            self.assertTrue(False)
