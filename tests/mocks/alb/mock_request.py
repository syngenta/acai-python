import base64
import json


def _alb_request_context():
    return {
        'elb': {
            'targetGroupArn': 'arn:aws:elasticloadbalancing:us-east-1:123456789012:targetgroup/acai-tg/50dc6c495c0c9188'
        }
    }


def get_basic_post():
    return {
        'requestContext': _alb_request_context(),
        'httpMethod': 'POST',
        'path': 'unit-test/v1/basic',
        'queryStringParameters': {
            'name': 'me'
        },
        'headers': {
            'x-api-key': 'SOME-KEY',
            'content-type': 'application/json',
            'host': 'mock-alb.example.com',
            'x-forwarded-for': '203.0.113.42',
            'x-forwarded-port': '443',
            'x-forwarded-proto': 'https',
        },
        'body': json.dumps({'body_key': 'body_value'}),
        'isBase64Encoded': False,
    }


def get_basic_post_base64():
    event = get_basic_post()
    event['body'] = base64.b64encode(event['body'].encode('utf-8')).decode('utf-8')
    event['isBase64Encoded'] = True
    return event


def get_raised_exception_post():
    return {
        'requestContext': _alb_request_context(),
        'httpMethod': 'POST',
        'path': 'unit-test/v1/raise-exception',
        'queryStringParameters': {},
        'headers': {
            'content-type': 'application/json',
            'host': 'mock-alb.example.com',
            'x-forwarded-for': '203.0.113.42',
        },
        'body': json.dumps({}),
        'isBase64Encoded': False,
    }


def get_unhandled_exception_post():
    return {
        'requestContext': _alb_request_context(),
        'httpMethod': 'POST',
        'path': 'unit-test/v1/unhandled-exception',
        'queryStringParameters': {},
        'headers': {
            'content-type': 'application/json',
            'host': 'mock-alb.example.com',
            'x-forwarded-for': '203.0.113.42',
        },
        'body': json.dumps({}),
        'isBase64Encoded': False,
    }


def get_dynamic_event(headers=None, path='', method='get', body=None, query=None):
    event = {
        'requestContext': _alb_request_context(),
        'httpMethod': method.upper(),
        'path': path,
        'queryStringParameters': query if query is not None else {},
        'headers': headers if headers is not None else {'content-type': 'application/json'},
        'body': json.dumps(body) if body is not None else '',
        'isBase64Encoded': False,
    }
    event['headers'].setdefault('host', 'mock-alb.example.com')
    return event
