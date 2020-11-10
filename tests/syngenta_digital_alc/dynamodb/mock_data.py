def get_old_data():
    return {
        'name': 'Paul',
        'contact': {
            'phone': '1111111111',
            'email': '1@1.com'
        },
        'favorite_colors':[
            'red',
            'blue'
        ]
    }


def get_complicated_data():
    return {
        'custom_details': [
            {
                'detail_type':'description',
                'detail_title':'description',
                'detail_description':'stuff 1',
                'display_timing':'always',
                'display_priority':0
            },
            {
                'detail_type':'request_reason',
                'detail_title':'request_reason',
                'detail_description':'stuff 2',
                'display_timing':'always',
                'display_priority':0
            }
        ]
    }


def get_mock_model_schema():
    return {
        'allOf': [
            {
                'type': 'object',
                'properties': {
                    'test_id':  {
                        'type': 'string'
                    },
                    'object_key': {
                        'type':'object',
                        'properties': {
                            'string_key': {
                                'type': 'string'
                            }
                        }
                    },
                    'array_number':{
                        'type':'array',
                        'items': {
                            'type': 'number'
                        }
                    },
                    'array_objects':{
                        'type':'array',
                        'items': {
                            'type':'object',
                            'properties': {
                                'array_string_key': {
                                    'type': 'string'
                                },
                                'array_number_key': {
                                    'type': 'number'
                                }
                            }
                        }
                    }
                }
            },
            {
                'required':[
                    'test_id',
                    'object_key',
                    'array_number',
                    'array_objects'
                ]
            }
        ]
    }


def get_mock_model_data():
    return {
        'test_id': 'abc123',
        'object_key': {
            'string_key': 'string'
        },
        'array_number':[1, 2, 3, 4],
        'array_objects': [
            {
                'array_string_key': 'array_string',
                'array_number_key': 5,
                'extra_key': {
                    'extra_child': 'extra_value'
                }
            },
            {
                'array_string_key': 'array_string_2',
                'array_number_key': 6
            }
        ],
        'extra_boolean': True
    }


def get_ddb_event():
    return {
        "Records": [
            {
                "eventID":"9a37c0d03eb60f7cf70cabc823de9907",
                "eventName":"INSERT",
                "eventVersion":"1.1",
                "eventSource":"aws:dynamodb",
                "awsRegion":"us-east-1",
                "dynamodb":{
                    "ApproximateCreationDateTime":1538695200.0,
                    "Keys":{
                        "example_id":{
                            "S":"123456789"
                        }
                    },
                    "NewImage":{
                        "example_id":{
                            "S":"123456789"
                        },
                        "note":{
                            "S":"Hosrawguw verrig zogupap ce so fajdis vub mos sif mawpowpug kif kihane."
                        },
                        "active":{
                            "BOOL":True
                        },
                        "personal":{
                            "M":{
                                "gender":{
                                    "S":"male"
                                },
                                "last_name":{
                                    "S":"Mcneil"
                                },
                                "first_name":{
                                    "S":"Mannix"
                                }
                            }
                        },
                        "transportation":{
                            "L":[
                                {
                                    "S":"public-transit"
                                },
                                {
                                    "S":"car-access"
                                }
                            ]
                        }
                    },
                    "SequenceNumber":"162100000000001439016707",
                    "SizeBytes":1124,
                    "StreamViewType":"NEW_AND_OLD_IMAGES"
                },
                'eventSourceARN': 'arn:aws:dynamodb:us-east-1:771875143460:table/test-example/stream/2019-10-04T23:18:26.340'
            }
        ]
    }
