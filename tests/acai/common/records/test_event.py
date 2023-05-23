import unittest

from acai.common.records.event import Event
from acai.common.records.record import Record

class MockDataClass:

    def __init__(self, record):
        self.record = record


class CommonRecordsTest(unittest.TestCase):
    event = {'key': 'value'}

    def test_event_accepts_event(self):
        event = Event(self.event)
        self.assertDictEqual(event.records[0].body, self.event)

    def test_event_accepts_event_list(self):
        event = Event([self.event])
        self.assertDictEqual(event.records[0].body, self.event)

    def test_event_returns_data_class(self):
        event = Event(self.event)
        event.data_class = MockDataClass
        self.assertTrue(isinstance(event.records[0], MockDataClass))
        self.assertTrue(isinstance(event.records[0].record, Record))

    def test_event_accepts_event_provides_raw_records(self):
        event = Event(self.event)
        self.assertDictEqual(event.raw_records[0], self.event)
