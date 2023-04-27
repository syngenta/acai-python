def get_basic_removed():
    return {
        'Records': [
            {
                'eventVersion': '2.0',
                'eventSource': 'aws: s3',
                'awsRegion': 'us-east-1',
                'eventTime': '2018-09-20T21: 10: 13.821Z',
                'eventName': 'ObjectRemoved: Put',
                'userIdentity': {
                    'principalId': 'AWS: AROAI7Z5ZQEQ3UETKKYGQ: deploy-workers-poc-put-v1-photo'
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
                        'name': 'user-preferences',
                        'ownerIdentity': {
                            'principalId': 'A32KFL0DQ3MH8X'
                        },
                        'arn': 'arn:aws:s3:::user-preferences'
                    },
                    'object': {
                        'key': 'user-1-prefs.json',
                        'size': 17545,
                        'eTag': 'b79ac2ef68c08fa9ac6013d53038a26c',
                        'sequencer': '005BA40CB5BD42013A'
                    }
                }
            }
        ]
    }


def get_basic():
    return {
        'Records': [
            {
                'eventVersion': '2.0',
                'eventSource': 'aws: s3',
                'awsRegion': 'us-east-1',
                'eventTime': '2018-09-20T21: 10: 13.821Z',
                'eventName': 'ObjectCreated: Put',
                'userIdentity': {
                    'principalId': 'AWS: AROAI7Z5ZQEQ3UETKKYGQ: deploy-workers-poc-put-v1-photo'
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
                        'name': 'user-preferences',
                        'ownerIdentity': {
                            'principalId': 'A32KFL0DQ3MH8X'
                        },
                        'arn': 'arn:aws:s3:::user-preferences'
                    },
                    'object': {
                        'key': 'user-1-prefs.json',
                        'size': 17545,
                        'eTag': 'b79ac2ef68c08fa9ac6013d53038a26c',
                        'sequencer': '005BA40CB5BD42013A'
                    }
                }
            }
        ]
    }


def get_basic_csv():
    return {
        'Records': [
            {
                'eventVersion': '2.0',
                'eventSource': 'aws: s3',
                'awsRegion': 'us-east-1',
                'eventTime': '2018-09-20T21: 10: 13.821Z',
                'eventName': 'ObjectCreated: Put',
                'userIdentity': {
                    'principalId': 'AWS:AROAI7Z5ZQEQ3UETKKYGQ:user-preferences'
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
                        'name': 'user-preferences',
                        'ownerIdentity': {
                            'principalId': 'A32KFL0DQ3MH8X'
                        },
                        'arn': 'arn:aws:s3:::user-preferences'
                    },
                    'object': {
                        'key': 'users.csv',
                        'size': 17545,
                        'eTag': 'b79ac2ef68c08fa9ac6013d53038a26c',
                        'sequencer': '005BA40CB5BD42013A'
                    }
                }
            }
        ]
    }

