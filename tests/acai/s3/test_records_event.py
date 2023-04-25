import unittest

from acai.s3.records_event import RecordsEvent
from acai.s3.record_event import RecordEvent

from tests.mocks.s3 import mock_event
from tests.mocks.s3.mock_data_class import MockS3DataClass


class RecordsEventTest(unittest.TestCase):
    basic_event = mock_event.get_basic()

    def test_records_event_accepts_event(self):
        records_event = RecordsEvent(self.basic_event)
        self.assertEqual(records_event.context, None)
        self.assertEqual(records_event.data_class, None)
        self.assertDictEqual(records_event.event, self.basic_event)
        self.assertEqual(len(records_event .records), len(self.basic_event['Records']))

    def test_records_event_returns_record_event(self):
        records_event = RecordsEvent(self.basic_event)
        self.assertTrue(isinstance(records_event.records[0], RecordEvent))

    def test_records_event_returns_data_class(self):
        records_event = RecordsEvent(self.basic_event)
        records_event.data_class = MockS3DataClass
        self.assertTrue(isinstance(records_event.records[0], MockS3DataClass))
        self.assertTrue(isinstance(records_event.records[0].record, RecordEvent))
