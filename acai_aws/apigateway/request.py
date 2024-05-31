import base64
import urllib

import xmltodict

from acai_aws.common.json_helper import JsonHelper


class Request:

    def __init__(self, event, lambda_context=None, timeout=None):
        self.__event = event
        self.lambda_context = lambda_context
        self.__timeout = timeout
        self.__body = event['body'] if event.get('body') is not None else {}
        self.__route = event['path'] if event.get('path') is not None else ''
        self.__path_params = event['pathParameters'] if event.get('pathParameters') is not None else ''
        self.__request_context = event['requestContext'] if event.get('requestContext') is not None else {}
        self.__domain = event.get('requestContext', {}).get('domainName', '')
        self.__stage = event.get('requestContext', {}).get('stage', '')
        self.__context = {}
        self.__parsers = {
            'application/json': 'json',
            'application/graphql': 'graphql',
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
            cookies = ';'.join(self.__event.get('cookies', []))
        return cookies

    @property
    def protocol(self):
        if self.__request_context.get('protocol'):
            protocol = self.__request_context.get('protocol', 'http')
        else:
            protocol = self.__request_context.get('http', {}).get('protocol', 'http')
        return 'https' if 'https' in protocol.lower() else 'http'

    @property
    def content_type(self):
        return self.headers.get('content-type', '').split(';')[0]

    @property
    def host_url(self):
        return f'{self.protocol}://{self.__domain}'

    @property
    def domain(self):
        return self.__domain

    @property
    def stage(self):
        return self.__stage

    @property
    def method(self):
        if self.__event.get('httpMethod') is not None:
            return self.__event['httpMethod'].lower()
        return ''

    @property
    def resource(self):
        if self.__event.get('resource') is not None:
            return self.__event['resource']
        return ''

    @property
    def path(self):
        if self.__event.get('path') is not None:
            return self.__event['path']
        return ''

    @property
    def route(self):
        if self.__route and self.__route[0] != '/':
            return f'/{self.__route}'
        return self.__route

    @route.setter
    def route(self, route):
        self.__route = route

    @property
    def authorizer(self):
        if self.__event.get('isOffline') is not None:
            return self.headers
        return self.__request_context.get('authorizer', self.headers)

    @property
    def headers(self):
        headers = {k.lower(): v for k, v in self.__event.get('headers', {}).items()}
        return headers

    @property
    def body(self):
        try:
            content_type = self.headers.get('content-type', '').split(';')[0]
            parser = self.__parsers.get(content_type, 'raw')
            return getattr(self, parser)
        except Exception as error:
            print(error)
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
        if self.__event.get('queryStringParameters') is not None:
            return self.__event['queryStringParameters']
        return {}

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
    def timeout(self):
        return self.__timeout

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
