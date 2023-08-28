import base64
import json
import unittest

from acai_aws.kinesis.record import Record

from tests.mocks.kinesis import mock_event


class KinesisRecordTest(unittest.TestCase):
    basic_record = mock_event.get_basic()['Records'][0]

    def test_record_accepts_event(self):
        record = Record(self.basic_record)
        self.assertEqual(record.operation, record.UNKNOWN)
        self.assertEqual(record.id, self.basic_record['eventID'])
        self.assertEqual(record.name, self.basic_record['eventName'])
        self.assertEqual(record.source, self.basic_record['eventSource'])
        self.assertEqual(record.source_arn, self.basic_record['eventSourceARN'])
        self.assertEqual(record.region, self.basic_record['awsRegion'])
        self.assertEqual(record.version, self.basic_record['eventVersion'])
        self.assertEqual(record.invoke_identity_arn, self.basic_record['invokeIdentityArn'])
        self.assertEqual(record.schema_version, self.basic_record['kinesis']['kinesisSchemaVersion'])
        self.assertEqual(record.partition_key, self.basic_record['kinesis']['partitionKey'])
        self.assertEqual(record.time_stamp, self.basic_record['kinesis']['approximateArrivalTimestamp'])
        self.assertEqual(record.sequence_number, self.basic_record['kinesis']['sequenceNumber'])
        self.assertEqual(record.data, json.loads(base64.b64decode(self.basic_record['kinesis']['data']).decode('utf-8')))
        self.assertEqual(record.body, json.loads(base64.b64decode(self.basic_record['kinesis']['data']).decode('utf-8')))

    def test_record_prints(self):
        try:
            record = Record(self.basic_record)
            print(record)
            self.assertTrue(True)
        except Exception as error:
            print(error)
            self.assertTrue(False)
