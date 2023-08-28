import base64
import json
import unittest

from acai_aws.firehose.record import Record

from tests.mocks.firehose import mock_event


class FirehoseRecordTest(unittest.TestCase):
    basic_record = mock_event.get_basic()['records'][0]

    def test_record_accepts_event(self):
        record = Record(self.basic_record)
        self.assertEqual(record.operation, record.UNKNOWN)
        self.assertDictEqual(record.body, json.loads(base64.b64decode(self.basic_record['data']).decode('utf-8')))
        self.assertEqual(record.record_id, self.basic_record['recordId'])
        self.assertEqual(record.epoc_time_stamp, self.basic_record['approximateArrivalTimestamp'])
        self.assertEqual(record.shard_id, self.basic_record['kinesisRecordMetadata']['shardId'])
        self.assertEqual(record.partition_key, self.basic_record['kinesisRecordMetadata']['partitionKey'])
        self.assertEqual(record.time_stamp, self.basic_record['kinesisRecordMetadata']['approximateArrivalTimestamp'])
        self.assertEqual(record.sequence_number, self.basic_record['kinesisRecordMetadata']['sequenceNumber'])
        self.assertEqual(record.subsequence_number, self.basic_record['kinesisRecordMetadata']['subsequenceNumber'])
        self.assertEqual(record.data, json.loads(base64.b64decode(self.basic_record['data']).decode('utf-8')))

    def test_record_prints(self):
        try:
            record = Record(self.basic_record)
            print(record)
            self.assertTrue(True)
        except Exception as error:
            print(error)
            self.assertTrue(False)
