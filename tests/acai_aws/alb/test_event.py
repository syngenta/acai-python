import json
import unittest

from acai_aws.alb.event import Event
from acai_aws.alb.record import Record

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

    def test_event_validate_invalid_body_builds_http_400_response(self):
        event = Event(self.basic_event, schema=self.schema_path, required_body='v1-alb-body-wrong')
        event.validate()
        response = event.build_short_circuit_response()
        self.assertIsNotNone(response)
        self.assertEqual(response['statusCode'], 400)
        self.assertEqual(response['headers']['Content-Type'], 'application/json')
        self.assertFalse(response['isBase64Encoded'])
        body = json.loads(response['body'])
        self.assertIn('errors', body)
        self.assertTrue(len(body['errors']) > 0)
        for error in body['errors']:
            self.assertIn('key_path', error)
            self.assertIn('message', error)

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

    def test_event_validate_invalid_body_with_dict_schema_builds_http_400(self):
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
        event.validate()
        response = event.build_short_circuit_response()
        self.assertIsNotNone(response)
        self.assertEqual(response['statusCode'], 400)
        body = json.loads(response['body'])
        self.assertIn('errors', body)
        self.assertTrue(len(body['errors']) > 0)

    def test_event_validate_valid_body_no_short_circuit(self):
        event = Event(self.basic_event, schema=self.schema_path, required_body='v1-alb-body')
        event.validate()
        self.assertIsNone(event.build_short_circuit_response())
        self.assertEqual(len(event.validation_errors), 0)

    def test_event_validate_no_required_body_no_short_circuit(self):
        event = Event(self.basic_event)
        event.validate()
        self.assertIsNone(event.build_short_circuit_response())

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
