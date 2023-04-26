import unittest
from moto import mock_s3
import boto3
import jsonpickle

from acai.s3.records_event import RecordsEvent
from acai.s3.record_event import RecordEvent

from tests.mocks.s3 import mock_event
from tests.mocks.s3.mock_data_class import MockS3DataClass


class RecordsEventTest(unittest.TestCase):
    basic_event = mock_event.get_basic()
    csv_event = mock_event.get_basic_csv()
    mock_s3 = mock_s3()
    starting_csv_string = ['Name,Job,Age,Income', 'Alice,Programmer,23,110000', 'Bob,Executive,34,90000', 'Carl,Sales,45,50000']
    expected_json_data = {
        'lang': 'en-us',
        'sms': False,
        'email': True,
        'push': True
    }
    expected_csv_data = [
        {'Name': 'Alice', 'Job': 'Programmer', 'Age': '23', 'Income': '110000'},
        {'Name': 'Bob', 'Job': 'Executive', 'Age': '34', 'Income': '90000'},
        {'Name': 'Carl', 'Job': 'Sales', 'Age': '45', 'Income': '50000'}
    ]

    def setUp(self):
        self.mock_s3.start()
        self.bucket_name = self.basic_event['Records'][0]['s3']['bucket']['name']
        self.s3_json_key = self.basic_event['Records'][0]['s3']['object']['key']
        self.s3_csv_key = self.csv_event['Records'][0]['s3']['object']['key']
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(self.bucket_name)
        bucket.create()
        json_data = jsonpickle.dumps(self.expected_json_data, unpicklable=False, use_decimal=True)
        json_data = bytes(json_data.encode('UTF-8'))
        s3_json_object = s3.Object(self.bucket_name, self.s3_json_key)
        s3_json_object.put(Body=json_data)
        csv_data = bytes('\n'.join(self.starting_csv_string).encode('UTF-8'))
        s3_csv_object = s3.Object(self.bucket_name, self.s3_csv_key)
        s3_csv_object.put(Body=csv_data)

    def tearDown(self):
        self.mock_s3.stop()

    def test_records_event_accepts_event(self):
        records_event = RecordsEvent(self.basic_event)
        self.assertEqual(records_event.context, None)
        self.assertEqual(records_event.data_class, None)
        self.assertDictEqual(records_event.event, self.basic_event)
        self.assertEqual(len(records_event .records), len(self.basic_event['Records']))

    def test_records_event_returns_record_event(self):
        records_event = RecordsEvent(self.basic_event)
        self.assertTrue(isinstance(records_event.records[0], RecordEvent))

    def test_records_event_returns_data_class(self):
        records_event = RecordsEvent(self.basic_event)
        records_event.data_class = MockS3DataClass
        self.assertTrue(isinstance(records_event.records[0], MockS3DataClass))
        self.assertTrue(isinstance(records_event.records[0].record, RecordEvent))

    def test_records_event_can_get_json_object(self):
        records_event = RecordsEvent(self.basic_event, get_object=True, data_type='json')
        self.assertDictEqual(records_event.records[0].body, self.expected_json_data)

    def test_records_event_can_get_csv_object(self):
        records_event = RecordsEvent(self.csv_event, get_object=True, data_type='csv')
        self.assertCountEqual(records_event.records[0].body, self.expected_csv_data)
