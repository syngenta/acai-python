import json

def get_aws_example():
    return {
        'resource': '/',
        'path': '/',
        'httpMethod': 'GET',
        'headers': {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'cookie': 's_fid=7AAB6XMPLAFD9BBF-0643XMPL09956DE2; regStatus=pre-register',
            'Host': '70ixmpl4fl.execute-api.us-east-2.amazonaws.com',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'upgrade-insecure-requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
            'X-Amzn-Trace-Id': 'Root=1-5e66d96f-7491f09xmpl79d18acf3d050',
            'X-Forwarded-For': '52.255.255.12',
            'X-Forwarded-Port': '443',
            'X-Forwarded-Proto': 'https'
        },
        'multiValueHeaders': {
            'accept': [
                'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
            ],
            'accept-encoding': [
                'gzip, deflate, br'
            ],
            'accept-language': [
                'en-US,en;q=0.9'
            ],
            'cookie': [
                's_fid=7AABXMPL1AFD9BBF-0643XMPL09956DE2; regStatus=pre-register;'
            ],
            'Host': [
                '70ixmpl4fl.execute-api.ca-central-1.amazonaws.com'
            ],
            'sec-fetch-dest': [
                'document'
            ],
            'sec-fetch-mode': [
                'navigate'
            ],
            'sec-fetch-site': [
                'none'
            ],
            'upgrade-insecure-requests': [
                '1'
            ],
            'User-Agent': [
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
            ],
            'X-Amzn-Trace-Id': [
                'Root=1-5e66d96f-7491f09xmpl79d18acf3d050'
            ],
            'X-Forwarded-For': [
                '52.255.255.12'
            ],
            'X-Forwarded-Port': [
                '443'
            ],
            'X-Forwarded-Proto': [
                'https'
            ]
        },
        'queryStringParameters': None,
        'multiValueQueryStringParameters': None,
        'pathParameters': None,
        'stageVariables': None,
        'requestContext': {
            'resourceId': '2gxmpl',
            'resourcePath': '/',
            'httpMethod': 'GET',
            'extendedRequestId': 'JJbxmplHYosFVYQ=',
            'requestTime': '10/Mar/2020:00:03:59 +0000',
            'path': '/Prod/',
            'accountId': '123456789012',
            'protocol': 'HTTP/1.1',
            'stage': 'Prod',
            'domainPrefix': '70ixmpl4fl',
            'requestTimeEpoch': 1583798639428,
            'requestId': '77375676-xmpl-4b79-853a-f982474efe18',
            'identity': {
                'cognitoIdentityPoolId': None,
                'accountId': None,
                'cognitoIdentityId': None,
                'caller': None,
                'sourceIp': '52.255.255.12',
                'principalOrgId': None,
                'accessKey': None,
                'cognitoAuthenticationType': None,
                'cognitoAuthenticationProvider': None,
                'userArn': None,
                'userAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
                'user': None
            },
            'domainName': '70ixmpl4fl.execute-api.us-east-2.amazonaws.com',
            'apiId': '70ixmpl4fl'
        },
        'body': json.dumps({'body_key': 'body_value'}),
        'isBase64Encoded': False
    }

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


def get_basic_for_validation():
    return {
        'headers': {
            'content-type': 'application/json'
        },
        'requestContext': {
            'resourceId': 't89kib',
            'authorizer': {
                'principalId': '9de3f415a97e410386dbef146e88744e',
                'integrationLatency': 572,
            }
        },
        'path': 'unit-test/v1/basic',
        'pathParameters': {
            'proxy': 'basic'
        },
        'resource': '/{proxy+}',
        'httpMethod': 'GET',
        'queryStringParameters': {
            'email': 'some-email'
        },
        'body': json.dumps({})
    }

def get_basic_passing_for_required_body_validation():
    return {
        'headers': {
            'content-type': 'application/json'
        },
        'requestContext': {
            'resourceId': 't89kib',
            'authorizer': {
                'principalId': '9de3f415a97e410386dbef146e88744e',
                'integrationLatency': 572,
            }
        },
        'path': 'unit-test/v1/basic',
        'pathParameters': {
            'proxy': 'basic'
        },
        'resource': '/{proxy+}',
        'httpMethod': 'GET',
        'queryStringParameters': {},
        'body': json.dumps({
            'id': 3,
            'email': 'some@email.com',
            'active': True,
            'favorites': ['anime', 'video games', 'basketball'],
            'notification_config': {
                'marketing': False,
                'transactions': True
            }
        })
    }

def get_basic_failing_for_required_body_validation():
    return {
        'headers': {
            'content-type': 'application/json'
        },
        'requestContext': {
            'resourceId': 't89kib',
            'authorizer': {
                'principalId': '9de3f415a97e410386dbef146e88744e',
                'integrationLatency': 572,
            }
        },
        'path': 'unit-test/v1/basic',
        'pathParameters': {
            'proxy': 'basic'
        },
        'resource': '/{proxy+}',
        'httpMethod': 'GET',
        'queryStringParameters': {},
        'body': json.dumps({
            'email': 'some@email.com',
            'active': True,
            'favorites': ['anime', 'video games', 'basketball'],
            'notification_config': {
                'marketing': False,
                'transactions': True
            }
        })
    }


def get_dynamic_event(**kwargs):
    return {
        'headers': kwargs.get('headers', {}),
        'requestContext': {
            'resourceId': 't89kib',
            'authorizer': {
                'principalId': '9de3f415a97e410386dbef146e88744e',
                'integrationLatency': 572,
            }
        },
        'path': kwargs.get('path', 'unit-test/v1/basic'),
        'pathParameters': {
            'proxy': kwargs.get('proxy', 'basic')
        },
        'resource': '/{proxy+}',
        'httpMethod': kwargs.get('method', 'GET').upper(),
        'queryStringParameters': kwargs.get('query', {}),
        'body': json.dumps(kwargs.get('body', {}))
    }

def get_auto_validated_data():
    return {
        'headers': {
            'x-api-key': 'some-key',
            'cookie': 's_fid=7AAB6XMPLAFD9BBF-0643XMPL09956DE2; regStatus=pre-register',
            'Host': 'localhost:3000',
            'Content-Type': 'application/json'
        },
        'requestContext': {
            'resourceId': 't89kib',
            'domainName': 'localhost:3000',
            'protocol': 'HTTP/1.1',
            'authorizer': {
                'principalId': '9de3f415a97e410386dbef146e88744e',
                'integrationLatency': 572,
            }
        },
        'path': '/unit-test/v1/auto',
        'pathParameters': {
            'proxy': 'auto'
        },
        'resource': '/{proxy+}',
        'httpMethod': 'POST',
        'queryStringParameters': {},
        'body': json.dumps({
            'test_id': 'abc123',
            'object_key': {
                'key': 'value'
            },
            'array_number': [1, 2, 3],
            'array_objects': [
                {
                    'array_string_key': 'string_value',
                    'array_number_key': 0
                }
            ]
        })
    }

def get_auto_validated_data_fails():
    return {
        'headers': {
            'x-api-key': 'some-key',
            'cookie': 's_fid=7AAB6XMPLAFD9BBF-0643XMPL09956DE2; regStatus=pre-register',
            'Host': 'localhost:3000',
            'Content-Type': 'application/json'
        },
        'requestContext': {
            'resourceId': 't89kib',
            'domainName': 'localhost:3000',
            'protocol': 'HTTP/1.1',
            'authorizer': {
                'principalId': '9de3f415a97e410386dbef146e88744e',
                'integrationLatency': 572,
            }
        },
        'path': '/unit-test/v1/auto',
        'pathParameters': {
            'proxy': 'auto'
        },
        'resource': '/{proxy+}',
        'httpMethod': 'POST',
        'queryStringParameters': {},
        'body': json.dumps({
            'object_key': {
                'key': 'value'
            },
            'array_number': [1, 2, 3],
            'array_objects': [
                {
                    'array_string_key': 'string_value',
                    'array_number_key': 0
                }
            ]
        })
    }
