import unittest
import json

from acai_aws.generic.event_client import EventClient
from tests.acai_aws.generic import mock_data


class ConsoleEventClientTest(unittest.TestCase):

    def setUp(self):
        self.raw_console_event = mock_data.get_event()
        self.event = EventClient(self.raw_console_event, None)

    def test_body(self):
        self.assertDictEqual(self.event.body, json.loads(self.raw_console_event))

    def test_raw_body(self):
        self.assertEqual(self.event.raw_body, self.raw_console_event)
