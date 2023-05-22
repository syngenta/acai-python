import base64
import json
import unittest

from acai.mq.record import Record

from tests.mocks.mq import mock_event


class MQRecordTest(unittest.TestCase):
    basic_record = mock_event.get_basic()['messages'][0]

    def test_record_accepts_event(self):
        record = Record(self.basic_record)
        self.assertEqual(record.operation, record.UNKNOWN)

    def test_record_prints(self):
        try:
            record = Record(self.basic_record)
            print(record)
            self.assertTrue(True)
        except Exception as error:
            print(error)
            self.assertTrue(False)
