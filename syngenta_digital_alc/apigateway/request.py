import base64
import urllib

import xmltodict

from syngenta_digital_alc.common.json_helper import JsonHelper


class Request:

    def __init__(self, event, lambda_context=None):
        self.__event = event
        self.__event_body = event.get('body', {})
        self.__route = event.get('path', '')
        self.__path_params = event.get('pathParameters', '')
        self.__context = {}
        self.__parsers = {
            'application/json': 'json',
            'application/graphql': 'json',
            'application/x-www-form-urlencoded': 'form',
            'multipart/form-data': 'raw',
            'application/xml': 'xml',
            'text/xml': 'xml',
            'raw': 'raw'
        }
        self.lambda_context = lambda_context

    @property
    def method(self):
        return self.__event.get('httpMethod', '').lower()

    @property
    def resource(self):
        return self.__event.get('resource', '')

    @property
    def path(self):
        return self.__event.get('path', '')

    @property
    def route(self):
        return self.__route

    @route.setter
    def route(self, route):
        self.__route = route

    @property
    def authorizer(self):
        if self.__event.get('isOffline'):
            return self.headers
        return self.__event.get('requestContext', {}).get('authorizer', self.headers)

    @property
    def headers(self):
        return self.__event.get('headers', {})

    @property
    def body(self):
        try:
            content_type = self.headers['content-type'].split(';')[0]
            parser = self.__parsers.get(content_type, 'raw')
            return getattr(self, parser)
        except Exception:
            return self.__event_body

    @property
    def json(self):
        return JsonHelper.decode(self.__event_body, True)

    @property
    def form(self):
        return dict(urllib.parse.parse_qsl(self.__event_body))

    @property
    def xml(self):
        return xmltodict.parse(self.__event_body)

    @property
    def graphql(self):
        try:
            request = base64.b64decode(self.__event_body).decode('utf-8')
        except Exception:
            request = self.__event_body
        return JsonHelper.decode(request)

    @property
    def raw(self):
        return self.__event_body

    @property
    def params(self):
        return {'query': self.query_params, 'path': self.path_params}

    @property
    def query_params(self):
        return self.__event.get('queryStringParameters', {})

    @property
    def path_params(self):
        return self.__path_params

    @path_params.setter
    def path_params(self, path_params):
        key, value = path_params
        self.__path_params[key] = value

    @property
    def context(self):
        return self.__context

    @context.setter
    def context(self, context):
        self.__context = context

    @property
    def event(self):
        return self.__event

    @property
    def complete(self):
        return {
            'method': self.method,
            'resource': self.resource,
            'headers': self.headers,
            'authorizer': self.authorizer,
            'params': self.params,
            'body': self.body,
            'context': self.context
        }

    def clear_path_params(self):
        self.__path_params = {}

    def __str__(self):
        return JsonHelper.encode(self.complete)
