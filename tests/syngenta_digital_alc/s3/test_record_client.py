import unittest

from syngenta_digital_alc.s3.record_client import RecordClient
from tests.syngenta_digital_alc.s3 import mock_data


class S3RecordClientTest(unittest.TestCase):

    def setUp(self):
        self.raw_record = mock_data.get_s3_event()['Records'][0]
        self.record = RecordClient(self.raw_record)

    def test_event_name(self):
        self.assertEqual(self.record.event_name, 'ObjectCreated:Put')

    def test_event_source(self):
        self.assertEqual(self.record.event_source, 'aws:s3')

    def test_event_version(self):
        self.assertEqual(self.record.event_version, '2.0')

    def test_event_time(self):
        self.assertEqual(self.record.event_time, '2018-09-20T21:10:13.821Z')

    def test_region(self):
        self.assertEqual(self.record.region, 'us-east-1')

    def test_request_parameters(self):
        self.assertDictEqual(self.record.request_parameters, {'sourceIPAddress': '172.20.133.36'})

    def test_response_elements(self):
        self.assertDictEqual(
            self.record.response_elements,
            {
                'x-amz-request-id': '6B859DD0CE613FAE',
                'x-amz-id-2': 'EXLMfc9aiXZFzNwLKXpw35iaVvl/DkEA6GtbuxjfmuLN3kLPL/aGoa7NMSwpl3m7ICAtNbjJX4w='
            }
        )

    def test_s3_configuration_id(self):
        self.assertEqual(self.record.s3_configuration_id, 'exS3-v2--7cde234c7ff76c53c44990396aeddc6d')

    def test_s3_object(self):
        self.assertDictEqual(
            self.record.s3_object,
            {
                'key': '123456789/3c8e97105d5f462f8896a7189910ee16-original.jpg',
                'size': 17545,
                'eTag': 'b79ac2ef68c08fa9ac6013d53038a26c',
                'sequencer': '005BA40CB5BD42013A'
            }
        )

    def test_s3_schema_version(self):
        self.assertEqual(self.record.s3_schema_version, '1.0')
