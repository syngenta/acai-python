import unittest

from acai_aws.alb.event import Event
from acai_aws.alb.record import Record
from acai_aws.common.records.exception import RecordException

from tests.mocks.alb import mock_event
from tests.mocks.alb.mock_data_class import MockALBDataClass


class ALBEventTest(unittest.TestCase):
    basic_event = mock_event.get_basic()
    schema_path = 'tests/mocks/alb/openapi.yml'
    expected_body = {
        'business_id': 'biz-e2e-001',
        'decision': 'APPROVED',
        'completed': '2026-03-30T12:40:40.353'
    }

    def test_event_accepts_event(self):
        event = Event(self.basic_event)
        self.assertEqual(event.context, None)
        self.assertEqual(event.data_class, None)
        self.assertDictEqual(event.event, self.basic_event)
        self.assertEqual(len(event.records), 1)

    def test_event_raw_records_wraps_single_event(self):
        event = Event(self.basic_event)
        self.assertEqual(len(event.raw_records), 1)
        self.assertDictEqual(event.raw_records[0], self.basic_event)

    def test_event_returns_record_instance(self):
        event = Event(self.basic_event)
        self.assertTrue(isinstance(event.records[0], Record))

    def test_event_returns_data_class(self):
        event = Event(self.basic_event)
        event.data_class = MockALBDataClass
        self.assertTrue(isinstance(event.records[0], MockALBDataClass))
        self.assertTrue(isinstance(event.records[0].record, Record))

    def test_event_filters_by_operations(self):
        event = Event(self.basic_event, operations=['created'])
        self.assertEqual(len(event.records), 1)

    def test_event_filters_out_non_matching_operations(self):
        event = Event(self.basic_event, operations=['deleted'])
        self.assertEqual(len(event.records), 0)

    def test_event_validate_record_body_with_schema_file(self):
        event = Event(self.basic_event, schema=self.schema_path, required_body='v1-alb-body')
        self.assertDictEqual(event.records[0].body, self.expected_body)

    def test_event_validate_filters_out_record_body_with_schema_file(self):
        event = Event(self.basic_event, schema=self.schema_path, required_body='v1-alb-body-wrong')
        self.assertEqual(len(event.records), 0)

    def test_event_validate_raises_exception_record_body_with_schema_file(self):
        try:
            event = Event(self.basic_event, schema=self.schema_path, required_body='v1-alb-body-wrong', raise_body_error=True)
            print(event.records)
            self.assertTrue(False)
        except RecordException as record_error:
            self.assertTrue(isinstance(record_error, RecordException))

    def test_event_validate_record_body_with_schema_dict(self):
        schema = {
            '$id': 'https://example.com/alb.schema.json',
            '$schema': 'https://json-schema.org/draft/2020-12/schema',
            'title': 'ALB',
            'type': 'object',
            'properties': {
                'business_id': {
                    'type': 'string'
                },
                'decision': {
                    'type': 'string'
                },
                'completed': {
                    'type': 'string'
                }
            }
        }
        event = Event(self.basic_event, schema=self.schema_path, required_body=schema)
        self.assertDictEqual(event.records[0].body, self.expected_body)

    def test_event_validate_raises_error_record_body_with_schema_dict(self):
        schema = {
            '$id': 'https://example.com/alb.schema.json',
            '$schema': 'https://json-schema.org/draft/2020-12/schema',
            'title': 'ALB',
            'type': 'object',
            'properties': {
                'business_id': {
                    'type': 'integer'
                },
                'decision': {
                    'type': 'string'
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
            '$id': 'https://example.com/alb.schema.json',
            '$schema': 'https://json-schema.org/draft/2020-12/schema',
            'title': 'ALB',
            'type': 'object',
            'properties': {
                'business_id': {
                    'type': 'integer'
                },
                'decision': {
                    'type': 'string'
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
