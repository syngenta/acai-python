def get_basic():
    return {
        'eventSource': 'aws:kafka',
        'eventSourceArn': 'arn:aws:kafka:sa-east-1:123456789012:cluster/vpc-2priv-2pub/751d2973-a626-431c-9d4e-d7975eb44dd7-2',
        'bootstrapServers': 'b-2.demo-cluster-1.a1bcde.c1.kafka.us-east-1.amazonaws.com:9092,b-1.demo-cluster-1.a1bcde.c1.kafka.us-east-1.amazonaws.com:9092',
        'records': {
            'mytopic-0': [
                {
                    'topic': 'mytopic',
                    'partition': 0,
                    'offset': 15,
                    'timestamp': 1545084650987,
                    'timestampType': 'CREATE_TIME',
                    'key': 'c29tZV9rZXk=',
                    'value': 'eyJsYW5nIjogImVuLXVzIiwgInNtcyI6IHRydWUsICJlbWFpbCI6IHRydWUsICJwdXNoIjogdHJ1ZX0=',
                    'headers': [
                        {
                            'headerKey': [
                                104,
                                101,
                                97,
                                100,
                                101,
                                114,
                                86,
                                97,
                                108,
                                117,
                                101
                            ]
                        }
                    ]
                }
            ]
        }
    }
