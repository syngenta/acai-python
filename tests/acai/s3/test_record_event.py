import unittest

from acai.s3.record_event import RecordEvent

from tests.mocks.s3 import mock_event


class RecordEventTest(unittest.TestCase):
    basic_record = mock_event.get_basic()['Records'][0]

    def test_record_event_accepts_event(self):
        record = RecordEvent(self.basic_record)
        self.assertIsNone(record.body)
        self.assertEqual(record.name, self.basic_record['eventName'])
        self.assertEqual(record.source, self.basic_record['eventSource'])
        self.assertEqual(record.version, self.basic_record['eventVersion'])
        self.assertEqual(record.time, self.basic_record['eventTime'])
        self.assertEqual(record.region, self.basic_record['awsRegion'])
        self.assertEqual(record.request, self.basic_record['requestParameters'])
        self.assertEqual(record.response, self.basic_record['responseElements'])
        self.assertEqual(record.configuration_id, self.basic_record['s3']['configurationId'])
        self.assertEqual(record.object, self.basic_record['s3']['object'])
        self.assertEqual(record.bucket, self.basic_record['s3']['bucket'])
        self.assertEqual(record.key, self.basic_record['s3']['object']['key'])
        self.assertEqual(record.user_identity, self.basic_record['userIdentity']['principalId'])
        self.assertEqual(record.operation, record.CREATED)

    def test_record_event_allows_body_to_be_set(self):
        expected = {'some_key': 'some_value'}
        record = RecordEvent(self.basic_record)
        record.body = expected.copy()
        self.assertDictEqual(record.body, expected)
