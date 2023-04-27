import unittest
from moto import mock_s3
import boto3
import jsonpickle

from acai.s3.records import Records
from acai.s3.record import Record
from acai.common.records.exception import RecordException

from tests.mocks.s3 import mock_event
from tests.mocks.s3.mock_data_class import MockS3DataClass


class S3RecordsTest(unittest.TestCase):
    basic_event = mock_event.get_basic()
    csv_event = mock_event.get_basic_csv()
    mock_s3 = mock_s3()
    schema_path = 'tests/mocks/s3/openapi.yml'
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

    def test_records_accepts_event(self):
        records = Records(self.basic_event)
        self.assertEqual(records.context, None)
        self.assertEqual(records.data_class, None)
        self.assertDictEqual(records.event, self.basic_event)
        self.assertEqual(len(records .records), len(self.basic_event['Records']))

    def test_records_returns_record_event(self):
        records = Records(self.basic_event)
        self.assertTrue(isinstance(records.records[0], Record))

    def test_records_returns_data_class(self):
        records = Records(self.basic_event)
        records.data_class = MockS3DataClass
        self.assertTrue(isinstance(records.records[0], MockS3DataClass))
        self.assertTrue(isinstance(records.records[0].record, Record))

    def test_records_can_get_json_object(self):
        records = Records(self.basic_event, get_object=True, data_type='json')
        self.assertDictEqual(records.records[0].body, self.expected_json_data)

    def test_records_can_get_csv_object(self):
        records = Records(self.csv_event, get_object=True, data_type='csv')
        self.assertCountEqual(records.records[0].body, self.expected_csv_data)

    def test_records_validate_record_body_with_schema_file(self):
        records = Records(
            self.basic_event,
            get_object=True,
            data_type='json',
            required_body='v1-s3-body',
            schema=self.schema_path
        )
        self.assertDictEqual(records.records[0].body, self.expected_json_data)

    def test_records_validate_filter_out_record_body_with_schema_file(self):
        records = Records(
            self.basic_event,
            get_object=True,
            data_type='json',
            schema=self.schema_path,
            required_body='v1-s3-body-wrong',
            raise_body_error=True
        )
        try:
            records.records
            self.assertTrue(False)
        except RecordException as record_error:
            self.assertTrue(isinstance(record_error, RecordException))
