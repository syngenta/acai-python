import json


def get_basic():
    return {
        'headers': {
            'x-api-key': 'SOME-KEY',
            'content-type': 'application/json'
        },
        'requestContext': {
            'resourceId': 't89kib',
            'authorizer': {
                'x-authorizer-key': 'SOME KEY',
                'principalId': '9de3f415a97e410386dbef146e88744e',
                'integrationLatency': 572,
            }
        },
        'path': 'unit-test/v1/basic',
        'pathParameters': {
            'proxy': 'hello'
        },
        'resource': '/{proxy+}',
        'httpMethod': 'GET',
        'queryStringParameters': {
            'name': 'me'
        },
        'body': json.dumps({'body_key': 'body_value'})
    }


def get_basic_offline():
    return {
        'isOffline': True,
        'headers': {
            'x-api-key': 'SOME-KEY',
            'x-authorizer-key': 'SOME KEY',
            'content-type': 'application/json'
        },
        'path': 'unit-test/v1/basic',
        'pathParameters': {
            'proxy': 'hello'
        },
        'resource': '/{proxy+}',
        'httpMethod': 'GET',
        'queryStringParameters': {
            'name': 'me'
        },
        'body': json.dumps({'body_key': 'body_value'})
    }


def get_basic_form():
    return {
        'headers': {
            'x-api-key': 'SOME-KEY',
            'x-authorizer-key': 'SOME KEY',
            'content-type': 'application/x-www-form-urlencoded'
        },
        'path': 'unit-test/v1/basic',
        'pathParameters': {
            'proxy': 'hello'
        },
        'resource': '/{proxy+}',
        'httpMethod': 'GET',
        'queryStringParameters': {
            'name': 'me'
        },
        'body': 'param1=data1&param2=data2&param3=data3'
    }


def get_basic_xml():
    return {
        'headers': {
            'x-api-key': 'SOME-KEY',
            'x-authorizer-key': 'SOME KEY',
            'content-type': 'application/xml'
        },
        'path': 'unit-test/v1/basic',
        'pathParameters': {
            'proxy': 'hello'
        },
        'resource': '/{proxy+}',
        'httpMethod': 'GET',
        'queryStringParameters': {
            'name': 'me'
        },
        'body': '<root xmlns="http://defaultns.com/" xmlns:a="http://a.com/" xmlns:b="http://b.com/"><x>1</x><a:y>2</a:y><b:z>3</b:z></root>'
    }


def get_basic_raw():
    return {
        'headers': {
            'x-api-key': 'SOME-KEY',
            'x-authorizer-key': 'SOME KEY'
        },
        'path': 'unit-test/v1/basic',
        'pathParameters': {
            'proxy': 'hello'
        },
        'resource': '/{proxy+}',
        'httpMethod': 'GET',
        'queryStringParameters': {
            'name': 'me'
        },
        'body': 'unit-test'
    }


def get_basic_graphql():
    return {
        'headers': {
            'x-api-key': 'SOME-KEY',
            'x-authorizer-key': 'SOME KEY',
            'content-type': 'application/graphql'
        },
        'path': 'unit-test/v1/basic',
        'pathParameters': {
            'proxy': 'hello'
        },
        'resource': '/{proxy+}',
        'httpMethod': 'GET',
        'queryStringParameters': {
            'name': 'me'
        },
        'body': '{players{name}}'
    }


def basic_graphql_variables():
    return {
        'headers': {
            'x-api-key': 'SOME-KEY',
            'x-authorizer-key': 'SOME KEY',
            'content-type': 'application/graphql'
        },
        'path': 'unit-test/v1/basic',
        'pathParameters': {
            'proxy': 'hello'
        },
        'resource': '/{proxy+}',
        'httpMethod': 'GET',
        'queryStringParameters': {
            'name': 'me'
        },
        'body': json.dumps(
            {
                'query': 'query GreetingQuery ($arg1: String) { hello (name: $arg1) { value } }',
                'operationName': 'GreetingQuery',
                'variables': {'arg1': 'Timothy'}
            }
        )
    }


def get_basic_nested():
    return {
        'headers': {
            'x-api-key': 'SOME-KEY',
            'content-type': 'application/json'
        },
        'requestContext': {
            'resourceId': 't89kib',
            'authorizer': {
                'x-authorizer-key': 'SOME KEY',
                'principalId': '9de3f415a97e410386dbef146e88744e',
                'integrationLatency': 572,
            }
        },
        'path': 'unit-test/v1/nested-1/nested-2/basic',
        'pathParameters': {
            'proxy': 'hello'
        },
        'resource': '/{proxy+}',
        'httpMethod': 'GET',
        'queryStringParameters': {
            'name': 'me'
        },
        'body': json.dumps({'body_key': 'body_value'})
    }


def get_basic_init():
    return {
        'headers': {
            'x-api-key': 'SOME-KEY',
            'content-type': 'application/json'
        },
        'requestContext': {
            'resourceId': 't89kib',
            'authorizer': {
                'x-authorizer-key': 'SOME KEY',
                'principalId': '9de3f415a97e410386dbef146e88744e',
                'integrationLatency': 572,
            }
        },
        'path': 'unit-test/v1/home/',
        'pathParameters': {
            'proxy': 'hello'
        },
        'resource': '/{proxy+}',
        'httpMethod': 'GET',
        'queryStringParameters': {
            'name': 'me'
        },
        'body': json.dumps({'body_key': 'body_value'})
    }


def get_dynamic():
    return {
        'headers': {
            'x-api-key': 'SOME-KEY',
            'content-type': 'application/json'
        },
        'requestContext': {
            'resourceId': 't89kib',
            'authorizer': {
                'x-authorizer-key': 'SOME KEY',
                'principalId': '9de3f415a97e410386dbef146e88744e',
                'integrationLatency': 572,
            }
        },
        'path': 'unit-test/v1/dynamic/1',
        'pathParameters': {
            'proxy': 'hello'
        },
        'resource': '/{proxy+}',
        'httpMethod': 'GET',
        'queryStringParameters': {
            'name': 'me'
        },
        'body': json.dumps({'body_key': 'body_value'})
    }


def get_bad_route():
    return {
        'headers': {
            'x-api-key': 'SOME-KEY',
            'content-type': 'application/json'
        },
        'requestContext': {
            'resourceId': 't89kib',
            'authorizer': {
                'x-authorizer-key': 'SOME KEY',
                'principalId': '9de3f415a97e410386dbef146e88744e',
                'integrationLatency': 572,
            }
        },
        'path': 'unit-test/v1/bad/route',
        'pathParameters': {
            'proxy': 'hello'
        },
        'resource': '/{proxy+}',
        'httpMethod': 'GET',
        'queryStringParameters': {
            'name': 'me'
        },
        'body': json.dumps({'body_key': 'body_value'})
    }


def get_basic_post():
    return {
        'headers': {
            'x-api-key': 'SOME-KEY',
            'content-type': 'application/json'
        },
        'requestContext': {
            'resourceId': 't89kib',
            'authorizer': {
                'x-authorizer-key': 'SOME KEY',
                'principalId': '9de3f415a97e410386dbef146e88744e',
                'integrationLatency': 572,
            }
        },
        'path': 'unit-test/v1/basic',
        'pathParameters': {
            'proxy': 'hello'
        },
        'resource': '/{proxy+}',
        'httpMethod': 'POST',
        'queryStringParameters': {
            'name': 'me'
        },
        'body': json.dumps({'body_key': 'body_value'})
    }


def get_dynamic_post():
    return {
        'headers': {
            'x-api-key': 'SOME-KEY',
            'content-type': 'application/json'
        },
        'requestContext': {
            'resourceId': 't89kib',
            'authorizer': {
                'x-authorizer-key': 'SOME KEY',
                'principalId': '9de3f415a97e410386dbef146e88744e',
                'integrationLatency': 572,
            }
        },
        'path': 'unit-test/v1/dynamic/1',
        'pathParameters': {},
        'resource': '/{proxy+}',
        'httpMethod': 'POST',
        'queryStringParameters': {
            'name': 'me'
        },
        'body': json.dumps({'body_key': 'body_value'})
    }

def get_bad_dynamic_post():
    return {
        'headers': {
            'x-api-key': 'SOME-KEY',
            'content-type': 'application/json'
        },
        'requestContext': {
            'resourceId': 't89kib',
            'authorizer': {
                'x-authorizer-key': 'SOME KEY',
                'principalId': '9de3f415a97e410386dbef146e88744e',
                'integrationLatency': 572,
            }
        },
        'path': 'unit-test/v1/bad_dynamic/1',
        'pathParameters': {},
        'resource': '/{proxy+}',
        'httpMethod': 'POST',
        'queryStringParameters': {
            'name': 'me'
        },
        'body': json.dumps({'body_key': 'body_value'})
    }

def get_no_dynamic_post():
    return {
        'headers': {
            'x-api-key': 'SOME-KEY',
            'content-type': 'application/json'
        },
        'requestContext': {
            'resourceId': 't89kib',
            'authorizer': {
                'x-authorizer-key': 'SOME KEY',
                'principalId': '9de3f415a97e410386dbef146e88744e',
                'integrationLatency': 572,
            }
        },
        'path': 'unit-test/v1/no_dynamic/1',
        'pathParameters': {},
        'resource': '/{proxy+}',
        'httpMethod': 'POST',
        'queryStringParameters': {
            'name': 'me'
        },
        'body': json.dumps({'body_key': 'body_value'})
    }


def get_raised_exception_post():
    return {
        'headers': {
            'x-api-key': 'SOME-KEY',
            'content-type': 'application/json'
        },
        'requestContext': {
            'resourceId': 't89kib',
            'authorizer': {
                'x-authorizer-key': 'SOME KEY',
                'principalId': '9de3f415a97e410386dbef146e88744e',
                'integrationLatency': 572,
            }
        },
        'path': 'unit-test/v1/raise-exception',
        'pathParameters': {
            'proxy': 'hello'
        },
        'resource': '/{proxy+}',
        'httpMethod': 'POST',
        'queryStringParameters': {
            'name': 'me'
        },
        'body': json.dumps({'body_key': 'body_value'})
    }


def get_unhandled_exception_post():
    return {
        'headers': {
            'x-api-key': 'SOME-KEY',
            'content-type': 'application/json'
        },
        'requestContext': {
            'resourceId': 't89kib',
            'authorizer': {
                'x-authorizer-key': 'SOME KEY',
                'principalId': '9de3f415a97e410386dbef146e88744e',
                'integrationLatency': 572,
            }
        },
        'path': 'unit-test/v1/unhandled-exception',
        'pathParameters': {
            'proxy': 'hello'
        },
        'resource': '/{proxy+}',
        'httpMethod': 'POST',
        'queryStringParameters': {
            'name': 'me'
        },
        'body': json.dumps({'body_key': 'body_value'})
    }
