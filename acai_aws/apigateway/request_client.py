import base64
import urllib.parse

from acai_aws.common import json_helper


class RequestClient:

    def __init__(self, event, context):
        self._event = event
        self.context = context

    @property
    def method(self):
        return self._event.get('httpMethod', {})

    @property
    def resource(self):
        return self._event.get('resource', {})

    @property
    def authorizer(self):
        if self._event.get('isOffline'):
            return self._event.get('headers')
        return self._event.get('requestContext', {}).get('authorizer', self._event.get('headers'))

    @property
    def headers(self):
        return self._event.get('headers', {})

    @property
    def body(self):
        return json_helper.try_decode_json(self._event.get('body', {}))

    @property
    def json(self):
        return json_helper.try_decode_json(self._event.get('body', {}))

    @property
    def graphql(self):
        try:
            if base64.b64encode(base64.b64decode(self._event.get('body'))) == self._event.get('body'):
                request = base64.b64decode(self._event.get('body'))
            else:
                request = self._event.get('body')
        except Exception:
            request = self._event.get('body')
        return json_helper.try_decode_json(request)

    @property
    def form_encoded(self):
        return dict(urllib.parse.parse_qsl(self._event.get('body', {})))

    @property
    def params(self):
        if self._event.get('queryStringParameters') is None:
            return {}
        return self._event.get('queryStringParameters')

    @property
    def path_parameters(self):
        return self._event.get('pathParameters', {})

    @property
    def request(self):
        return {
            'http_method': self.method,
            'resource': self.resource,
            'headers': self.headers,
            'authorizer': self.authorizer,
            'params': self.params,
            'path_parameters': self.path_parameters,
            'body': self.body
        }

    def __str__(self):
        return str({
            'request': self.request
        })
