import unittest

from acai_aws.generic.event import Event


class GenericEventTest(unittest.TestCase):
    basic_event = {'key': 'value'}

    def test_event_accepts_event(self):
        event = Event(self.basic_event)
        self.assertDictEqual(self.basic_event, event.body)
