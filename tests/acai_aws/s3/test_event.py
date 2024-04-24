import unittest
from moto import mock_aws
import boto3
import jsonpickle

from acai_aws.s3.event import Event
from acai_aws.s3.record import Record
from acai_aws.common.records.exception import RecordException

from tests.mocks.s3 import mock_event
from tests.mocks.s3.mock_data_class import MockS3DataClass


class S3EventTest(unittest.TestCase):
    basic_event = mock_event.get_basic()
    csv_event = mock_event.get_basic_csv()
    mock_aws = mock_aws()
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
        self.mock_aws.start()
        self.bucket_name = self.basic_event['Records'][0]['s3']['bucket']['name']
        self.s3_json_key = self.basic_event['Records'][0]['s3']['object']['key']
        self.s3_csv_key = self.csv_event['Records'][0]['s3']['object']['key']
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(self.bucket_name)
        bucket.create(CreateBucketConfiguration={'LocationConstraint': 'us-east-2'})
        json_data = jsonpickle.dumps(self.expected_json_data, unpicklable=False, use_decimal=True)
        json_data = bytes(json_data.encode('UTF-8'))
        s3_json_object = s3.Object(self.bucket_name, self.s3_json_key)
        s3_json_object.put(Body=json_data)
        csv_data = bytes('\n'.join(self.starting_csv_string).encode('UTF-8'))
        s3_csv_object = s3.Object(self.bucket_name, self.s3_csv_key)
        s3_csv_object.put(Body=csv_data)

    def tearDown(self):
        self.mock_aws.stop()

    def test_event_accepts_event(self):
        event = Event(self.basic_event)
        self.assertEqual(event.context, None)
        self.assertEqual(event.data_class, None)
        self.assertDictEqual(event.event, self.basic_event)
        self.assertEqual(len(event.records), len(self.basic_event['Records']))

    def test_event_returns_record_event(self):
        event = Event(self.basic_event)
        self.assertTrue(isinstance(event.records[0], Record))

    def test_event_returns_data_class(self):
        event = Event(self.basic_event)
        event.data_class = MockS3DataClass
        self.assertTrue(isinstance(event.records[0], MockS3DataClass))
        self.assertTrue(isinstance(event.records[0].record, Record))

    def test_event_can_get_json_object(self):
        event = Event(self.basic_event, get_object=True, data_type='json')
        self.assertDictEqual(event.records[0].body, self.expected_json_data)

    def test_event_can_get_csv_object(self):
        event = Event(self.csv_event, get_object=True, data_type='csv')
        self.assertCountEqual(event.records[0].body, self.expected_csv_data)

    def test_event_validate_record_body_with_schema_file(self):
        event = Event(
            self.basic_event,
            get_object=True,
            data_type='json',
            required_body='v1-s3-body',
            schema=self.schema_path
        )
        self.assertDictEqual(event.records[0].body, self.expected_json_data)

    def test_event_validate_record_body_with_schema_dict(self):
        schema = {
            '$id': 'https://example.com/person.schema.json',
            '$schema': 'https://json-schema.org/draft/2020-12/schema',
            'title': 'Person',
            'type': 'object',
            "properties": {
                'lang': {
                    'type': 'string'
                },
                'sms': {
                    'type': 'boolean'
                },
                'email': {
                    'type': 'boolean'
                },
                'push': {
                    'type': 'boolean'
                }
            }
        }
        event = Event(
            self.basic_event,
            get_object=True,
            data_type='json',
            required_body='v1-s3-body',
            schema=schema
        )
        self.assertDictEqual(event.records[0].body, self.expected_json_data)

    def test_event_errors_record_body_with_schema_dict(self):
        schema = {
            '$id': 'https://example.com/person.schema.json',
            '$schema': 'https://json-schema.org/draft/2020-12/schema',
            'title': 'Person',
            'type': 'object',
            "properties": {
                'lang': {
                    'type': 'integer'
                },
                'sms': {
                    'type': 'boolean'
                },
                'email': {
                    'type': 'boolean'
                },
                'push': {
                    'type': 'boolean'
                }
            }
        }
        event = Event(
            self.basic_event,
            get_object=True,
            data_type='json',
            required_body='v1-s3-body',
            schema=schema,
            raise_body_error=True
        )
        try:
            print(event.records)
            self.assertTrue(False)
        except RecordException as record_error:
            self.assertTrue(isinstance(record_error, RecordException))

    def test_event_validate_filters_out_record_body_with_schema_file(self):
        event = Event(
            self.basic_event,
            get_object=True,
            data_type='json',
            schema=self.schema_path,
            required_body='v1-s3-body-wrong'
        )
        self.assertEqual(len(event.records), 0)

    def test_event_validate_errors_out_record_body_with_schema_file(self):
        event = Event(
            self.basic_event,
            get_object=True,
            data_type='json',
            schema=self.schema_path,
            required_body='v1-s3-body-wrong',
            raise_body_error=True
        )
        try:
            print(event.records)
            self.assertTrue(False)
        except RecordException as record_error:
            self.assertTrue(isinstance(record_error, RecordException))

    def test_event_raw_records(self):
        event = Event(self.basic_event)
        self.assertCountEqual(event.raw_records, self.basic_event['Records'])

    def test_event_print(self):
        event = Event(self.basic_event)
        try:
            print(event)
            self.assertTrue(True)
        except Exception as error:
            print(error)
            self.assertTrue(False)
