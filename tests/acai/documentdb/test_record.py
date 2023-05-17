import json
import unittest

from acai.documentdb.record import Record

from tests.mocks.documentdb import mock_event


class DocumentDBRecordTest(unittest.TestCase):
    basic_record = mock_event.get_basic()['events'][0]

    def test_record_accepts_event(self):
        record = Record(self.basic_record)
        event = self.basic_record.get('event')
        self.assertEqual(record.operation, record.CREATED)
        self.assertEqual(record.event_id, event.get('_id', {}).get('_data'))
        self.assertEqual(record.cluster_time, '2023-02-16T23:06:15.900000')
        self.assertEqual(record.document_key, event.get('documentKey', {}).get('_id', {}).get('$oid'))
        self.assertEqual(record.full_document, event['fullDocument'])
        self.assertEqual(record.change_event, event['operationType'])
        self.assertEqual(record.db, event.get('ns', {}).get('db'))
        self.assertEqual(record.collection, event.get('ns', {}).get('coll'))

    def test_record_prints(self):
        try:
            record = Record(self.basic_record)
            print(record)
            self.assertTrue(True)
        except Exception as error:
            print(error)
            self.assertTrue(False)
