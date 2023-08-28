import unittest

from acai_aws.sqs.event_client import EventClient
from tests.acai_aws.sqs import mock_data


class SQSEventClientTest(unittest.TestCase):

    def setUp(self):
        self.raw_sqs_event = mock_data.get_sqs_event()
        self.sqs_event = EventClient(self.raw_sqs_event, None)
        self.record = self.sqs_event.records[0]

    def test_raw_records(self):
        self.assertEqual(self.sqs_event.raw_records, self.raw_sqs_event['Records'])

    def test_records(self):
        self.assertEqual(len(self.sqs_event.records), 1)
