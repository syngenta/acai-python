import json
import unittest

from syngenta_digital_alc.sqs.record_client import RecordClient
from tests.syngenta_digital_alc.sqs import mock_data


class SQSRecordClientTest(unittest.TestCase):

    def setUp(self):
        self.raw_record = mock_data.get_sqs_event()['Records'][0]
        self.record = RecordClient(self.raw_record)

    def test_message_id(self):
        self.assertEqual(self.record.message_id, "c80e8021-a70a-42c7-a470-796e1186f753")

    def test_receipt_handle(self):
        self.assertEqual(
            self.record.receipt_handle,
            "AQEBJQ+/u6NsnT5t8Q/VbVxgdUl4TMKZ5FqhksRdIQvLBhwNvADoBxYSOVeCBXdnS9P+"
        )

    def tets_body(self):
        self.assertEqual(self.record.body, json.loads("{\"foo\":\"bar\"}"))

    def test_raw_body(self):
        self.assertEqual(self.record.raw_body, "{\"foo\":\"bar\"}")

    def test_attributes(self):
        self.assertEqual(
            self.record.attributes,
            {
                "ApproximateReceiveCount": "3",
                "SentTimestamp": "1529104986221",
                "SenderId": "594035263019",
                "ApproximateFirstReceiveTimestamp": "1529104986230"
            }
        )

    def test_approximate_receive_count(self):
        self.assertEqual(self.record.approximate_receive_count, "3")

    def test_sent_timestamp(self):
        self.assertEqual(self.record.sent_timestamp, "1529104986221")

    def test_sender_id(self):
        self.assertEqual(self.record.sender_id, "594035263019")

    def test_approximate_first_receive_timestamp(self):
        self.assertEqual(self.record.approximate_first_receive_timestamp, "1529104986230")

    def test_message_attributes(self):
        self.assertDictEqual(self.record.message_attributes, {'attribute': 'this is an attribute'})

    def test_md5_of_body(self):
        self.assertEqual(self.record.md5_of_body, '9bb58f26192e4ba00f01e2e7b136bbd8')

    def test_event_source_arn(self):
        self.assertEqual(self.record.event_source_arn, 'arn:aws:sqs:us-west-2:123456789012:MyQueue')

    def test_region(self):
        self.assertEqual(self.record.region, 'us-west-2')
