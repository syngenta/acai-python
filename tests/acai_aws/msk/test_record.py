import base64
import json
import unittest

from acai_aws.msk.record import Record

from tests.mocks.msk import mock_event


class MSKRecordTest(unittest.TestCase):
    basic_record = mock_event.get_basic()['records']['mytopic-0'][0]

    def test_record_accepts_event(self):
        record = Record(self.basic_record)
        self.assertEqual(record.operation, record.UNKNOWN)
        self.assertEqual(record.topic, self.basic_record['topic'])
        self.assertEqual(record.partition, self.basic_record['partition'])
        self.assertEqual(record.offset, self.basic_record['offset'])
        self.assertEqual(record.time_stamp, self.basic_record['timestamp'])
        self.assertEqual(record.time_stamp_type, self.basic_record['timestampType'])
        self.assertEqual(record.key, base64.b64decode(self.basic_record['key']).decode('utf-8'))
        self.assertDictEqual(record.value, json.loads(base64.b64decode(self.basic_record['value']).decode('utf-8')))
        self.assertDictEqual(record.body, json.loads(base64.b64decode(self.basic_record['value']).decode('utf-8')))
        self.assertListEqual(record.headers, self.basic_record['headers'])

    def test_record_prints(self):
        try:
            record = Record(self.basic_record)
            print(record)
            self.assertTrue(True)
        except Exception as error:
            print(error)
            self.assertTrue(False)
