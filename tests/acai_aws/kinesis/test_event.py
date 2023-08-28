import unittest

from acai_aws.kinesis.event import Event
from acai_aws.kinesis.record import Record
from acai_aws.common.records.exception import RecordException

from tests.mocks.kinesis import mock_event
from tests.mocks.kinesis.mock_data_class import MockKinesisDataClass


class FirehoseEventTest(unittest.TestCase):
    basic_event = mock_event.get_basic()
    schema_path = 'tests/mocks/kinesis/openapi.yml'
    expected_body = {
        'lang': 'en-us',
        'sms': True,
        'email': True,
        'push': True
    }

    def test_event_accepts_event(self):
        event = Event(self.basic_event)
        self.assertEqual(event.context, None)
        self.assertEqual(event.data_class, None)
        self.assertDictEqual(event.event, self.basic_event)
        self.assertEqual(len(event.records), len(self.basic_event['Records']))

    def test_event_raw_records(self):
        event = Event(self.basic_event)
        self.assertCountEqual(event.raw_records, self.basic_event['Records'])

    def test_event_returns_record_event(self):
        event = Event(self.basic_event)
        self.assertTrue(isinstance(event.records[0], Record))

    def test_event_returns_data_class(self):
        event = Event(self.basic_event)
        event.data_class = MockKinesisDataClass
        self.assertTrue(isinstance(event.records[0], MockKinesisDataClass))
        self.assertTrue(isinstance(event.records[0].record, Record))

    def test_event_validate_record_body_with_schema_file(self):
        event = Event(self.basic_event, schema=self.schema_path, required_body='v1-kinesis-body')
        self.assertDictEqual(event.records[0].body, self.expected_body)

    def test_event_validate_filters_out_record_body_with_schema_file(self):
        event = Event(self.basic_event, schema=self.schema_path, required_body='v1-kinesis-body-wrong')
        self.assertEqual(len(event.records), 0)

    def test_event_validate_raises_exception_record_body_with_schema_file(self):
        try:
            event = Event(self.basic_event, schema=self.schema_path, required_body='v1-kinesis-body-wrong', raise_body_error=True)
            print(event.records)
            self.assertTrue(False)
        except RecordException as record_error:
            self.assertTrue(isinstance(record_error, RecordException))

    def test_event_validate_record_body_with_schema_dict(self):
        schema = {
            '$id': 'https://example.com/person.schema.json',
            '$schema': 'https://json-schema.org/draft/2020-12/schema',
            'title': 'Person',
            'type': 'object',
            "properties": {
                'lang': {
                    'type': 'string'
                },
                'sms': {
                    'type': 'boolean'
                },
                'email': {
                    'type': 'boolean'
                },
                'push': {
                    'type': 'boolean'
                }
            }
        }
        event = Event(self.basic_event, schema=self.schema_path, required_body=schema)
        self.assertDictEqual(event.records[0].body, self.expected_body)

    def test_event_validate_raises_error_record_body_with_schema_dict(self):
        schema = {
            '$id': 'https://example.com/person.schema.json',
            '$schema': 'https://json-schema.org/draft/2020-12/schema',
            'title': 'Person',
            'type': 'object',
            "properties": {
                'lang': {
                    'type': 'integer'
                },
                'sms': {
                    'type': 'boolean'
                },
                'email': {
                    'type': 'boolean'
                },
                'push': {
                    'type': 'boolean'
                }
            }
        }
        try:
            event = Event(self.basic_event, schema=self.schema_path, required_body=schema, raise_body_error=True)
            print(event.records)
            self.assertTrue(False)
        except RecordException as record_error:
            self.assertTrue(isinstance(record_error, RecordException))

    def test_event_validate_filters_out_record_body_with_schema_dict(self):
        schema = {
            '$id': 'https://example.com/person.schema.json',
            '$schema': 'https://json-schema.org/draft/2020-12/schema',
            'title': 'Person',
            'type': 'object',
            "properties": {
                'lang': {
                    'type': 'integer'
                },
                'sms': {
                    'type': 'boolean'
                },
                'email': {
                    'type': 'boolean'
                },
                'push': {
                    'type': 'boolean'
                }
            }
        }
        event = Event(self.basic_event, schema=self.schema_path, required_body=schema)
        self.assertEqual(len(event.records), 0)

    def test_event_print(self):
        event = Event(self.basic_event)
        try:
            print(event)
            self.assertTrue(True)
        except Exception as error:
            print(error)
            self.assertTrue(False)
