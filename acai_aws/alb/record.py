import base64

from acai_aws.common.json_helper import JsonHelper
from acai_aws.base.record import BaseRecord


class Record(BaseRecord):

    def __init__(self, record):
        super().__init__(record)
        self._http_operations = {
            'POST': self.CREATED,
            'PUT': self.UPDATED,
            'PATCH': self.UPDATED,
            'DELETE': self.DELETED
        }

    @property
    def body(self):
        raw_body = self._record.get('body', '')
        if self._record.get('isBase64Encoded') and raw_body:
            raw_body = base64.b64decode(raw_body).decode('utf-8')
        return JsonHelper.decode(raw_body)

    @property
    def operation(self):
        return self._http_operations.get(self.http_method, self.UNKNOWN)

    @property
    def http_method(self):
        return self._record.get('httpMethod')

    @property
    def path(self):
        return self._record.get('path')

    @property
    def headers(self):
        return self._record.get('headers', {})

    @property
    def query_params(self):
        return self._record.get('queryStringParameters', {})

    @property
    def source_ip(self):
        return self.headers.get('x-forwarded-for')

    @property
    def target_group_arn(self):
        return self._record.get('requestContext', {}).get('elb', {}).get('targetGroupArn')

    def __str__(self):
        return str({
            'body': self.body,
            'operation': self.operation,
            'http_method': self.http_method,
            'path': self.path,
            'headers': self.headers,
            'query_params': self.query_params,
            'source_ip': self.source_ip,
            'target_group_arn': self.target_group_arn
        })
