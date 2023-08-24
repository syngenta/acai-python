def get_basic():
    return {
        'invocationId': 'invoked123',
        'deliveryStreamArn': 'aws:lambda:events',
        'region': 'us-west-2',
        'records': [
            {
                'data': 'eyJsYW5nIjogImVuLXVzIiwgInNtcyI6IHRydWUsICJlbWFpbCI6IHRydWUsICJwdXNoIjogdHJ1ZX0=',
                'recordId': 'record1',
                'approximateArrivalTimestamp': 1510772160000,
                'kinesisRecordMetadata': {
                    'shardId': 'shardId-000000000000',
                    'partitionKey': '4d1ad2b9-24f8-4b9d-a088-76e9947c317a',
                    'approximateArrivalTimestamp': '2012-04-23T18:25:43.511Z',
                    'sequenceNumber': '49546986683135544286507457936321625675700192471156785154',
                    'subsequenceNumber': ''
                }
            }
        ]
    }
