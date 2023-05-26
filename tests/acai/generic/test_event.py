import unittest

from acai.generic.event import Event

from tests.mocks.generic.mock_class import MockDataClass


class GenericEventTest(unittest.TestCase):
    basic_event = {'key': 'value'}

    def test_event_accepts_event(self):
        event = Event(self.basic_event)
        self.assertDictEqual(self.basic_event, event.body)

    def test_event_accepts_data_class(self):
        event = Event(self.basic_event)
        event.data_class = MockDataClass
        self.assertTrue(isinstance(event.body, MockDataClass))


