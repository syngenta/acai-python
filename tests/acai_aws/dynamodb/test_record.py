import unittest

from acai_aws.dynamodb.record import Record

from tests.mocks.dynamodb import mock_event


class DynamoDBRecordTest(unittest.TestCase):
    created_record = mock_event.get_created_event()['Records'][0]
    updated_record = mock_event.get_updated_event()['Records'][0]
    deleted_record = mock_event.get_deleted_event()['Records'][0]

    def test_record_accepts_event(self):
        record = Record(self.created_record)
        expected_keys = {'example_id': '123456789'}
        expected_body = {
            'example_id': '123456789',
            'note': 'Hosrawguw verrig zogupap ce so fajdis vub mos sif mawpowpug kif kihane.',
            'active': True,
            'personal': {
                'gender': 'male',
                'last_name': 'Mcneil',
                'first_name': 'Mannix'
            },
            'transportation': ['public-transit', 'car-access']
        }
        self.assertDictEqual(record.body, expected_body)
        self.assertDictEqual(record.new_image, expected_body)
        self.assertDictEqual(record.old_image, {})
        self.assertEqual(record.name, self.created_record['eventName'])
        self.assertEqual(record.source_arn, self.created_record['eventSourceARN'])
        self.assertEqual(record.source, self.created_record['eventSource'])
        self.assertEqual(record.version, self.created_record['eventVersion'])
        self.assertEqual(record.id, self.created_record['eventID'])
        self.assertEqual(record.region, self.created_record['awsRegion'])
        self.assertEqual(record.stream_view_type, self.created_record['dynamodb']['StreamViewType'])
        self.assertEqual(record.sequence_number, self.created_record['dynamodb']['SequenceNumber'])
        self.assertEqual(record.size_bytes, self.created_record['dynamodb']['SizeBytes'])
        self.assertEqual(record.keys, expected_keys)
        self.assertEqual(record.approximate_creation_time, self.created_record['dynamodb']['ApproximateCreationDateTime'])
        self.assertEqual(record.operation, record.CREATED)

    def test_record_accepts_updated_event(self):
        record = Record(self.updated_record)
        self.assertEqual(record.operation, record.UPDATED)

    def test_record_accepts_deleted_event(self):
        record = Record(self.deleted_record)
        self.assertEqual(record.operation, record.DELETED)

    def test_record_accepts_unknown_event(self):
        unknown_event = self.deleted_record.copy()
        del unknown_event['dynamodb']['OldImage']
        record = Record(unknown_event)
        self.assertEqual(record.operation, record.UNKNOWN)

    def test_record_prints(self):
        try:
            record = Record(self.created_record)
            print(record)
            self.assertTrue(True)
        except Exception as error:
            print(error)
            self.assertTrue(False)
