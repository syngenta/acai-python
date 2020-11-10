import unittest

from syngenta_digital_alc.sns.record_client import RecordClient
from tests.syngenta_digital_alc.sns import mock_data


class SNSRecordClientTest(unittest.TestCase):

    def setUp(self):
        self.raw_record = mock_data.get_sns_event()['Records'][0]
        self.record = RecordClient(self.raw_record)

    def test_event_source(self):
        self.assertEqual(self.record.event_source, 'aws:sns')

    def test_event_version(self):
        self.assertEqual(self.record.event_version, '1.0')

    def test_event_subscription_arn(self):
        self.assertEqual(self.record.event_subscription_arn, 'eventsubscriptionarn')

    def test_sns_signature_version(self):
        self.assertEqual(self.record.sns_signature_version, '1')

    def test_sns_timestamp(self):
        self.assertEqual(self.record.sns_timestamp, '1970-01-01T00:00:00.000Z')

    def test_sns_signature(self):
        self.assertEqual(self.record.sns_signature, 'EXAMPLE')

    def test_sns_signing_cert_url(self):
        self.assertEqual(self.record.sns_signing_cert_url, 'EXAMPLE')

    def test_sns_message(self):
        self.assertEqual(self.record.sns_message, 'Hello from SNS!')

    def test_sns_message_attributes(self):
        self.assertDictEqual(
            self.record.sns_message_attributes,
            {
                'Test': {
                    'Type': 'String',
                    'Value': 'TestString'
                },
                'TestBinary': {
                    'Type': 'Binary', 'Value': 'TestBinary'
                }
            }
        )

    def test_sns_type(self):
        self.assertEqual(self.record.sns_type, 'Notification')

    def test_sns_unsubscribe_url(self):
        self.assertEqual(self.record.sns_unsubscribe_url, 'EXAMPLE')

    def test_sns_topic_arn(self):
        self.assertEqual(self.record.sns_topic_arn, 'topicarn')

    def test_sns_subject(self):
        self.assertEqual(self.record.sns_subject, 'TestInvoke')
