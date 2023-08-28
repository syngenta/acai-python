import base64
import json


def apigateway_event():
    return {
        'headers': {
            'x-api-key': 'SOME-KEY'
        },
        'requestContext': {
            'resourceId':'t89kib',
            'authorizer':{
                'x-authorizer-key': 'SOME KEY',
                'principalId':'9de3f415a97e410386dbef146e88744e',
                'integrationLatency':572,
            }
        },
        'pathParameters': {
            'proxy': 'hello'
        },
        'resource': '/{proxy+}',
        'httpMethod': 'GET',
        'queryStringParameters': {
            'name': 'me'
        },
        'body': json.dumps({'body_key':'body_value'})
    }

def apigateway_event_graphql(b64 = False):
    query = '''
    query {
        characters {
            results {
                name
                status
                species
                type
                gender
            }
        }
    }
    '''
    body = json.dumps({'query': query})
    if b64:
        body = base64.b64encode(body.encode('utf-8'))
    return {
        'headers': {
            'x-api-key': 'SOME-KEY'
        },
        'requestContext': {
            'resourceId':'t89kib',
            'authorizer':{
                'x-authorizer-key': 'SOME KEY',
                'principalId':'9de3f415a97e410386dbef146e88744e',
                'integrationLatency':572,
            }
        },
        'pathParameters': {
            'proxy': 'hello'
        },
        'resource': '/{proxy+}',
        'httpMethod': 'GET',
        'queryStringParameters': {
            'name': 'me'
        },
        'body': body
    }

def apigateway_event_form_encoded():
    return {
        'headers': {
            'x-api-key': 'SOME-KEY'
        },
        'requestContext': {
            'resourceId':'t89kib',
            'authorizer':{
                'x-authorizer-key': 'SOME KEY',
                'principalId':'9de3f415a97e410386dbef146e88744e',
                'integrationLatency':572,
            }
        },
        'pathParameters': {
            'proxy': 'hello'
        },
        'resource': '/{proxy+}',
        'httpMethod': 'GET',
        'queryStringParameters': {
            'name': 'me'
        },
        'body': 'tracking_code=4081141452&status=Complete&cpu_hours=0.006002831527777777&result_url=https%3a%2f%2fs3.amazonaws.com%2ffielddata.onsiteag.com%2f20210506%2f6499361e-1d72-4fbf-86be-663edc56f840%2fOnsiteProcessed_20210506_201030.zip%3fAWSAccessKeyId%3dAKIA3TR2EEYUQT5E23PG%26Expires%3d1622949031%26Signature%3dck8zjmWbMweHVIit0j9e%252BeGsGQw%253D&message='
    }

def apigateway_route(fail=''):
    return {
        'path': '/unit-tests/syngenta_digital_alc/mock-handler{}'.format(fail),
        'httpMethod': 'GET'
    }

def apigateway_event_with_body(condition):
    return {
        'headers': {
            'x-api-key': 'SOME-KEY'
        },
        'requestContext': {
            'resourceId':'t89kib',
            'authorizer':{
                'x-authorizer-key': 'SOME KEY',
                'principalId':'9de3f415a97e410386dbef146e88744e',
                'integrationLatency':572,
            }
        },
        'pathParameters': {
            'proxy': 'hello'
        },
        'resource': '/{proxy+}',
        'httpMethod': 'GET',
        'queryStringParameters': {
            'name': 'me'
        },
        'body': json.dumps(valid_request() if condition == 'pass' else bad_request())
    }

def request_schema():
    return {
        'type': 'object',
        'properties': {
            'test_id': {
                'type': 'string'
            },
            'object_key': {
                'type': 'object',
                'properties': {
                    'string_key': {
                    'type': 'string'
                    }
                }
            },
            'array_number': {
                'type': 'array',
                'items': {
                    'type': 'number'
                }
            },
            'array_objects': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'array_string_key': {
                            'type': 'string'
                        },
                        'array_number_key': {
                            'type': 'number'
                            }
                    }
                }
            },
            'fail_id': {
                'type': 'string'
            }
        },
        'required': [
            'test_id',
            'object_key',
            'array_number', 'array_objects'
        ],
        'additionalProperties': False
    }

def bad_request():
    return {
        'test_id': 1,
        'object_key': {
            'string_key': 'string'
        },
        'array_number': [],
        'array_objects': [{'array_string_key': 2, 'array_number_key': '1'}]
    }

def valid_request():
    return {
        'test_id': '1',
        'object_key': {
            'string_key': 'string'
        },
        'array_number': [1,2,3],
        'array_objects': [{'array_string_key': '2', 'array_number_key': 3}]
    }
