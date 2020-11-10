import simplejson as json

def get_sqs_event():
    return {
        "Records": [
            {
                "messageId": "c80e8021-a70a-42c7-a470-796e1186f753",
                "receiptHandle": "AQEBJQ+/u6NsnT5t8Q/VbVxgdUl4TMKZ5FqhksRdIQvLBhwNvADoBxYSOVeCBXdnS9P+",
                "body": "{\"foo\":\"bar\"}",
                "attributes": {
                    "ApproximateReceiveCount": "3",
                    "SentTimestamp": "1529104986221",
                    "SenderId": "594035263019",
                    "ApproximateFirstReceiveTimestamp": "1529104986230"
                },
                "messageAttributes": {'attribute': 'this is an attribute'},
                "md5OfBody": "9bb58f26192e4ba00f01e2e7b136bbd8",
                "eventSource": "aws:sqs",
                "eventSourceARN": "arn:aws:sqs:us-west-2:123456789012:MyQueue",
                "awsRegion": "us-west-2"
            }
        ]
    }

def get_sqs_sns_event():
    return {
        'Records': [
            {
                'messageId': '9c2a063c-98b7-4b05-8bbd-e16f52f100d8',
                'receiptHandle': 'AQEBYfNs5d1R8Q/uboUm/mdjwIiacjJE=',
                'body': json.dumps({
                    'Type': 'Notification',
                    'MessageId': 'e2f1ae2e-ee1e-58eb-8eb1-fae7293b2eb8',
                    'TopicArn': 'arn:aws:sns:us-east-1:771875143460:clocking-poc-events',
                    'Message': json.dumps({
                        'message': {
                            'event': 'Worker clocked out',
                            'context': {
                                'item': {'Key Sent From SNS': 'Value'},
                                'meta': {
                                    'version': '1.1.1',
                                    'message_format': 'json',
                                    'destination': 'sns'
                                }
                            }
                        }
                    }),
                    'Timestamp': '2019-01-29T03:13:41.459Z',
                    'SignatureVersion': '1',
                    'Signature': 'TX+gJ+wIyDKpAHLPL2Rd4gbNxOcQwpL0Vtp7zt',
                    'SigningCertURL': 'https://sns.us-east-1.amazonaws.com/SimpleNotificationService-ac565b8b1a6c5d002d285f9598aa1d9b.pem',
                    'UnsubscribeURL': 'https://sns.us-east-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=ARN',
                    'MessageAttributes': {
                        'message.event': {
                            'Type': 'String',
                            'Value': 'Event happened'
                        }
                    }
                }),
                'attributes': {
                    'ApproximateReceiveCount': '1',
                    'SentTimestamp': '1548731621524',
                    'SenderId': 'AIDAIT2UOQQY3AUEKVGXU',
                    'ApproximateFirstReceiveTimestamp': '1548731621538'
                },
                'messageAttributes': {},
                'md5OfBody': 'a165de1aba0f7dba96cef22bc4307efb',
                'eventSource': 'aws:sqs',
                'eventSourceARN': 'arn:aws:sqs:us-east-1:771875143460:clock-actions-poc-poc-incoming_clock_in',
                'awsRegion': 'us-east-1'
            }
        ]
    }
