import unittest

from acai_aws.sns.event_client import EventClient
from acai_aws.sns.record_client import RecordClient
from tests.acai_aws.sns import mock_data


class SNSEventClientTest(unittest.TestCase):

    def test_sns_record_doesnt_parse(self):
        framework = EventClient(mock_data.get_sns_event(), None)
        sns_record = framework.records[0]
        self.assertDictEqual(
            sns_record._record,
            {
                "EventVersion": "1.0",
                "EventSubscriptionArn": 'eventsubscriptionarn',
                "EventSource": "aws:sns",
                "Sns": {
                    "SignatureVersion": "1",
                    "Timestamp": "1970-01-01T00:00:00.000Z",
                    "Signature": "EXAMPLE",
                    "SigningCertUrl": "EXAMPLE",
                    "MessageId": "95df01b4-ee98-5cb9-9903-4c221d41eb5e",
                    "Message": "Hello from SNS!",
                    "MessageAttributes": {
                        "Test": {
                            "Type": "String",
                            "Value": "TestString"
                        },
                        "TestBinary": {
                            "Type": "Binary",
                            "Value": "TestBinary"
                        }
                    },
                    "Type": "Notification",
                    "UnsubscribeUrl": "EXAMPLE",
                    "TopicArn": 'topicarn',
                    "Subject": "TestInvoke"
                }
            }
        )

    def test_sns_record_parses(self):
        framework = EventClient(mock_data.get_sns_event(), None)
        sns_record = framework.records[0]
        self.assertIsInstance(sns_record, RecordClient)
