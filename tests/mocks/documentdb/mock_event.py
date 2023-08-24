def get_basic(operation='insert'):
    return {
        'eventSourceArn': 'arn:aws:rds:us-east-1:123456789012:cluster:canaryclusterb2a659a2-qo5tcmqkcl03',
        'events': [
            {
                'event': {
                    '_id': {
                        '_data': '0163eeb6e7000000090100000009000041e1'
                    },
                    'clusterTime': {
                        '$timestamp': {
                            't': 1676588775,
                            'i': 9
                        }
                    },
                    'documentKey': {
                        '_id': {
                            '$oid': '63eeb6e7d418cd98afb1c1d7'
                        }
                    },
                    'fullDocument': {
                        '_id': {
                            '$oid': '63eeb6e7d418cd98afb1c1d7'
                        },
                        'lang': 'en-us',
                        'sms': True,
                        'email': True,
                        'push': True
                    },
                    'ns': {
                        'db': 'test_database',
                        'coll': 'test_collection'
                    },
                    'operationType': operation
                }
            }
        ],
        'eventSource': 'aws:docdb'
    }