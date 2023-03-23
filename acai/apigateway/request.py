import base64
import urllib

import xmltodict

from acai.common.json_helper import JsonHelper


class Request:

    def __init__(self, event, lambda_context=None):
        self.lambda_context = lambda_context
        self.__event = event
        self.__body = event.get('body', {})
        self.__route = event.get('path', '')
        self.__path_params = event.get('pathParameters', '')
        self.__request_context = event.get('requestContext', {})
        self.__host_url = event.get('requestContext', {}).get('domainName', '')
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

    @property
    def cookies(self):
        if self.__event.get('headers', {}).get('cookie'):
            cookies = self.__event.get('headers', {}).get('cookie')
        else:
            cookies = self.__event.get('cookies', '')
        return cookies

    @property
    def protocol(self):
        if self.__request_context.get('protocol'):
            protocol = self.__request_context.get('protocol', 'http')
        else:
            protocol = self.__request_context.get('http', {}).get('protocol', 'http')
        return 'https' if 'https' in protocol.lower() else 'http'

    @property
    def host_url(self):
        return f'{self.protocol}://{self.__host_url}'

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
        return self.__request_context.get('authorizer', self.headers)

    @property
    def headers(self):
        headers = {k.lower(): v for k, v in self.__event.get('headers', {}).items()}
        return headers

    @property
    def body(self):
        try:
            content_type = self.headers['content-type'].split(';')[0]
            parser = self.__parsers.get(content_type, 'raw')
            return getattr(self, parser)
        except Exception as error:
            print(repr(error))
            return self.__body

    @property
    def json(self):
        return JsonHelper.decode(self.__body, True)

    @property
    def form(self):
        return dict(urllib.parse.parse_qsl(self.__body))

    @property
    def xml(self):
        return xmltodict.parse(self.__body)

    @property
    def graphql(self):
        try:
            request = base64.b64decode(self.__body).decode('utf-8')
        except Exception as error:
            print(error)
            request = self.__body
        return JsonHelper.decode(request)

    @property
    def raw(self):
        return self.__body

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
    def full(self):
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
        return JsonHelper.encode(self.full)
