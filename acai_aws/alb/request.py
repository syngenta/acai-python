import base64

from acai_aws.apigateway.request import Request as ApigatewayRequest


class Request(ApigatewayRequest):

    def __init__(self, event, lambda_context=None, timeout=None):
        if event.get('isBase64Encoded') and event.get('body'):
            event = {
                **event,
                'body': base64.b64decode(event['body']).decode('utf-8'),
                'isBase64Encoded': False,
            }
        super().__init__(event, lambda_context, timeout)

    @property
    def target_group_arn(self):
        return self.event.get('requestContext', {}).get('elb', {}).get('targetGroupArn', '')

    @property
    def source_ip(self):
        return self.headers.get('x-forwarded-for', '')
