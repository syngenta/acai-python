import unittest

from acai.dynamodb.records import Records
from acai.dynamodb.record import Record

from tests.mocks.dynamodb import mock_event


class DynamoDBRecordsTest(unittest.TestCase):
    created_event = mock_event.get_created_event()
    updated_event = mock_event.get_updated_event()
    deleted_event = mock_event.get_deleted_event()
    schema_path = 'tests/mocks/dynamodb/openapi.yml'

    def test_records_accepts_event(self):
        records = Records(self.created_event)
        self.assertEqual(records.context, None)
        self.assertEqual(records.data_class, None)
        self.assertDictEqual(records.event, self.created_event)
        self.assertEqual(len(records.records), len(self.created_event['Records']))
