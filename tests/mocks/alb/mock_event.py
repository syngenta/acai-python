import base64
import json


def get_basic(http_method='POST'):
    return {
        'requestContext': {
            'elb': {
                'targetGroupArn': 'arn:aws:elasticloadbalancing:us-east-1:123456789012:targetgroup/my-target-group/50dc6c495c0c9188'
            }
        },
        'httpMethod': http_method,
        'path': '/v1/kyc/callback',
        'queryStringParameters': {
            'status': 'approved',
            'ref': 'abc-123'
        },
        'headers': {
            'content-type': 'application/json',
            'host': '10.84.140.68',
            'x-forwarded-for': '10.104.8.48',
            'x-forwarded-port': '80',
            'x-forwarded-proto': 'http'
        },
        'body': '{"business_id": "biz-e2e-001", "decision": "APPROVED", "completed": "2026-03-30T12:40:40.353"}',
        'isBase64Encoded': False
    }


def get_base64():
    body = json.dumps({'business_id': 'biz-e2e-002', 'decision': 'DENIED'})
    return {
        'requestContext': {
            'elb': {
                'targetGroupArn': 'arn:aws:elasticloadbalancing:us-east-1:123456789012:targetgroup/my-target-group/50dc6c495c0c9188'
            }
        },
        'httpMethod': 'POST',
        'path': '/v1/kyc/callback',
        'queryStringParameters': {},
        'headers': {
            'content-type': 'application/json',
            'host': '10.84.140.68',
            'x-forwarded-for': '10.104.8.48',
            'x-forwarded-port': '80',
            'x-forwarded-proto': 'http'
        },
        'body': base64.b64encode(body.encode('utf-8')).decode('utf-8'),
        'isBase64Encoded': True
    }
