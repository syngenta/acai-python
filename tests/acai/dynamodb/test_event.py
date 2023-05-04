import unittest

from acai.dynamodb.event import Event
from acai.dynamodb.record import Record

from tests.mocks.dynamodb import mock_event


class DynamoDBRecordsTest(unittest.TestCase):
    created_event = mock_event.get_created_event()
    updated_event = mock_event.get_updated_event()
    deleted_event = mock_event.get_deleted_event()
    schema_path = 'tests/mocks/dynamodb/openapi.yml'

    def test_records_accepts_event(self):
        event = Event(self.created_event)
        self.assertEqual(event.context, None)
        self.assertEqual(event.data_class, None)
        self.assertDictEqual(event.event, self.created_event)
        self.assertEqual(len(event.records), len(self.created_event['Records']))
