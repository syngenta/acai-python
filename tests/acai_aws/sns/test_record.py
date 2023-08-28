import json
import unittest

from acai_aws.sns.record import Record

from tests.mocks.sns import mock_event


class SNSRecordTest(unittest.TestCase):
    basic_record = mock_event.get_basic()['Records'][0]

    def test_record_accepts_event(self):
        expected_attributes = {'Test': 'TestString', 'TestBinary': 'TestBinary'}
        record = Record(self.basic_record)
        self.assertEqual(record.version, self.basic_record['EventVersion'])
        self.assertEqual(record.subscription_arn, self.basic_record['EventSubscriptionArn'])
        self.assertEqual(record.source, self.basic_record['EventSource'])
        self.assertEqual(record.signature_version, self.basic_record['Sns']['SignatureVersion'])
        self.assertEqual(record.timestamp, self.basic_record['Sns']['Timestamp'])
        self.assertEqual(record.signature, self.basic_record['Sns']['Signature'])
        self.assertEqual(record.signing_cert_url, self.basic_record['Sns']['SigningCertUrl'])
        self.assertEqual(record.message_id, self.basic_record['Sns']['MessageId'])
        self.assertEqual(record.message, self.basic_record['Sns']['Message'])
        self.assertEqual(record.message_attributes, self.basic_record['Sns']['MessageAttributes'])
        self.assertDictEqual(record.attributes, expected_attributes)
        self.assertEqual(record.sns_type, self.basic_record['Sns']['Type'])
        self.assertEqual(record.unsubscribe_url, self.basic_record['Sns']['UnsubscribeUrl'])
        self.assertEqual(record.topic_arn, self.basic_record['Sns']['TopicArn'])
        self.assertEqual(record.subject, self.basic_record['Sns']['Subject'])
        self.assertDictEqual(record.body, json.loads(self.basic_record['Sns']['Message']))
        self.assertEqual(record.operation, record.UNKNOWN)

    def test_record_prints(self):
        try:
            record = Record(self.basic_record)
            print(record)
            self.assertTrue(True)
        except Exception as error:
            print(error)
            self.assertTrue(False)
