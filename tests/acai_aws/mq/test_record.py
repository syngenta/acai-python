import base64
import json
import unittest

from acai_aws.mq.record import Record

from tests.mocks.mq import mock_event


class MQRecordTest(unittest.TestCase):
    basic_record = mock_event.get_basic()['messages'][0]

    def test_record_accepts_event(self):
        record = Record(self.basic_record)
        self.assertEqual(record.operation, record.UNKNOWN)
        self.assertEqual(record.message_id, self.basic_record['messageID'])
        self.assertEqual(record.message_type, self.basic_record['messageType'])
        self.assertDictEqual(record.data, json.loads(base64.b64decode(self.basic_record['data'])))
        self.assertEqual(record.delivery_mode, self.basic_record['deliveryMode'])
        self.assertEqual(record.reply_to, self.basic_record['replyTo'])
        self.assertEqual(record.expiration, self.basic_record['expiration'])
        self.assertEqual(record.record_type, self.basic_record['type'])
        self.assertEqual(record.priority, self.basic_record['priority'])
        self.assertEqual(record.correlation_id, self.basic_record['correlationId'])
        self.assertEqual(record.redelivered, self.basic_record['redelivered'])
        self.assertEqual(record.destination, self.basic_record['destination'])
        self.assertEqual(record.properties, self.basic_record['properties'])
        self.assertEqual(record.time_stamp, self.basic_record['timestamp'])
        self.assertEqual(record.in_time, self.basic_record['brokerInTime'])
        self.assertEqual(record.out_time, self.basic_record['brokerOutTime'])
        self.assertDictEqual(record.body, json.loads(base64.b64decode(self.basic_record['data'])))

    def test_record_prints(self):
        try:
            record = Record(self.basic_record)
            print(record)
            self.assertTrue(True)
        except Exception as error:
            print(error)
            self.assertTrue(False)
