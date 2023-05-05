import json
import unittest

from acai.common.records.record import CommonRecord


class CommonRecordsTest(unittest.TestCase):
    record = {'key': 'value'}

    def test_record_accepts_event(self):
        record = CommonRecord(self.record)
        self.assertDictEqual(record.body, self.record)

    def test_record_body_decodes_json(self):
        json_record = json.dumps(self.record)
        record = CommonRecord(json_record)
        self.assertDictEqual(record.body, self.record)

    def test_record_has_unknown_operation(self):
        record = CommonRecord(self.record)
        self.assertEqual(record.operation, record.UNKNOWN)
