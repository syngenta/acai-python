import unittest

from syngenta_digital_alc.s3.event_client import EventClient
from syngenta_digital_alc.s3.record_client import RecordClient
from tests.syngenta_digital_alc.s3 import mock_data


class S3EventClientTest(unittest.TestCase):

    def test_s3_record_parses(self):
        framework = EventClient(mock_data.get_s3_event())
        s3_record = framework.records[0]
        self.assertIsInstance(s3_record, RecordClient)

    def test_s3_parsed_object(self):
        framework = EventClient(mock_data.get_s3_event())
        record = framework.records[0]
        self.assertDictEqual(
            record.s3_object,
            {
                'key': '123456789/3c8e97105d5f462f8896a7189910ee16-original.jpg',
                'size': 17545,
                'eTag': 'b79ac2ef68c08fa9ac6013d53038a26c',
                'sequencer': '005BA40CB5BD42013A'
            }
        )
        self.assertDictEqual(
            record.s3_bucket,
            {
                'name': 'deploy-workers-poc-photos',
                'ownerIdentity': {'principalId': 'A32KFL0DQ3MH8X'},
                'arn': 'arn:aws:s3:::deploy-workers-poc-photos'
            }
        )

    def test_s3_record_doesnt_parse(self):
        framework = EventClient(mock_data.get_s3_event())
        record = framework.records[0]
        self.assertDictEqual(
            record._record,
            {
                'eventVersion': '2.0',
                'eventSource': 'aws:s3',
                'awsRegion': 'us-east-1',
                'eventTime': '2018-09-20T21:10:13.821Z',
                'eventName': 'ObjectCreated:Put',
                'userIdentity': {
                    'principalId': 'AWS:AROAI7Z5ZQEQ3UETKKYGQ:deploy-workers-poc-put-v1-photo'
                },
                'requestParameters': {
                    'sourceIPAddress': '172.20.133.36'
                },
                'responseElements': {
                    'x-amz-request-id': '6B859DD0CE613FAE',
                    'x-amz-id-2': 'EXLMfc9aiXZFzNwLKXpw35iaVvl/DkEA6GtbuxjfmuLN3kLPL/aGoa7NMSwpl3m7ICAtNbjJX4w='
                },
                's3': {
                    's3SchemaVersion': '1.0',
                    'configurationId': 'exS3-v2--7cde234c7ff76c53c44990396aeddc6d',
                    'bucket': {
                        'name': 'deploy-workers-poc-photos',
                        'ownerIdentity': {
                            'principalId': 'A32KFL0DQ3MH8X'
                        },
                        'arn': 'arn:aws:s3:::deploy-workers-poc-photos'
                    },
                    'object': {
                        'key': '123456789/3c8e97105d5f462f8896a7189910ee16-original.jpg',
                        'size': 17545,
                        'eTag': 'b79ac2ef68c08fa9ac6013d53038a26c',
                        'sequencer': '005BA40CB5BD42013A'
                    }
                }
            }
        )
