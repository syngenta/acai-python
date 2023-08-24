def get_basic():
    return {
        'eventSource': 'aws:mq',
        'eventSourceArn': 'arn:aws:mq:us-west-2:111122223333:broker:test:b-9bcfa592-423a-4942-879d-eb284b418fc8',
        'messages': [
            {
                'messageID': 'ID:b-9bcfa592-423a-4942-879d-eb284b418fc8-1.mq.us-west-2.amazonaws.com-37557-1234520418293-4:1:1:1:1',
                'messageType': 'jms/text-message',
                'deliveryMode': 1,
                'replyTo': None,
                'type': None,
                'expiration': '60000',
                'priority': 1,
                'correlationId': 'myJMSCoID',
                'redelivered': False,
                'destination': {
                    'physicalName': 'testQueue'
                },
                'data': 'eyJsYW5nIjogImVuLXVzIiwgInNtcyI6IHRydWUsICJlbWFpbCI6IHRydWUsICJwdXNoIjogdHJ1ZX0=',
                'timestamp': 1598827811958,
                'brokerInTime': 1598827811958,
                'brokerOutTime': 1598827811959,
                'properties': {
                    'index': '1',
                    'doAlarm': 'false',
                    'myCustomProperty': 'value'
                }
            }
        ]
    }
