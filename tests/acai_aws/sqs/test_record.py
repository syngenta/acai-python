import json
import unittest

from acai_aws.sqs.record import Record

from tests.mocks.sqs import mock_event


class SQSRecordTest(unittest.TestCase):
    basic_record = mock_event.get_basic()['Records'][0]
    expected_attributes = {
        'ApproximateReceiveCount': '1',
        'SentTimestamp': '1545082649183',
        'SenderId': 'AIDAIENQZJOLO23YVJ4VO',
        'ApproximateFirstReceiveTimestamp': '1545082649185',
        'SomeString': 'Some String',
        'SomeBinary': 'Some Binary'
    }

    def test_record_accepts_event(self):
        record = Record(self.basic_record)
        self.assertEqual(record.operation, record.UNKNOWN)
        self.assertDictEqual(record.body, json.loads(self.basic_record['body']))
        self.assertEqual(record.message_id, self.basic_record['messageId'])
        self.assertEqual(record.receipt_handle, self.basic_record['receiptHandle'])
        self.assertEqual(record.message_attributes, self.basic_record['messageAttributes'])
        self.assertEqual(record.region, self.basic_record['awsRegion'])
        self.assertEqual(record.source_arn, self.basic_record['eventSourceARN'])
        self.assertEqual(record.source, self.basic_record['eventSource'])
        self.assertEqual(record.md5_of_body, self.basic_record['md5OfBody'])
        self.assertEqual(record.attributes, self.expected_attributes)

    def test_record_prints(self):
        try:
            record = Record(self.basic_record)
            print(record)
            self.assertTrue(True)
        except Exception as error:
            print(error)
            self.assertTrue(False)
