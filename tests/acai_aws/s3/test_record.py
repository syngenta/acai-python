import unittest

from acai_aws.s3.record import Record

from tests.mocks.s3 import mock_event


class S3RecordTest(unittest.TestCase):
    basic_record = mock_event.get_basic()['Records'][0]
    removed_record = mock_event.get_basic_removed()['Records'][0]
    unknown_record = mock_event.get_basic_unknown()['Records'][0]

    def test_record_event_accepts_event(self):
        record = Record(self.basic_record)
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
        self.assertEqual(record.bucket, self.basic_record['s3']['bucket']['name'])
        self.assertEqual(record.bucket_arn, self.basic_record['s3']['bucket']['arn'])
        self.assertEqual(record.bucket_owner, self.basic_record['s3']['bucket']['ownerIdentity']['principalId'])
        self.assertEqual(record.key, self.basic_record['s3']['object']['key'])
        self.assertEqual(record.schema_version, self.basic_record['s3']['s3SchemaVersion'])
        self.assertEqual(record.user_identity, self.basic_record['userIdentity']['principalId'])
        self.assertEqual(record.operation, record.CREATED)

    def test_record_event_accepts_remove_event(self):
        record = Record(self.removed_record)
        self.assertEqual(record.operation, record.DELETED)

    def test_record_event_accepts_unknown_event(self):
        record = Record(self.unknown_record)
        self.assertEqual(record.operation, record.UNKNOWN)

    def test_record_event_allows_body_to_be_set(self):
        expected = {'some_key': 'some_value'}
        record = Record(self.basic_record)
        record.body = expected.copy()
        self.assertDictEqual(record.body, expected)

    def test_record_event_prints(self):
        try:
            record = Record(self.basic_record)
            print(record)
            self.assertTrue(True)
        except Exception as error:
            print(error)
            self.assertTrue(False)
