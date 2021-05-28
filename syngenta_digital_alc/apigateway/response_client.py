import base64
import gzip
from io import BytesIO

import simplejson as json

from syngenta_digital_alc.common import json_helper


class ResponseClient:

    def __init__(self):
        self.__body = {}
        self.__code = 200
        self.__base64_encoded = False
        self.__compress = False
        self.__headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': '*'
        }

    @property
    def headers(self):
        return self.__headers

    @headers.setter
    def headers(self, value):
        key, val = value
        self.__headers[key] = val

    @property
    def base64_encoded(self):
        return self.__base64_encoded

    @base64_encoded.setter
    def base64_encoded(self, value):
        self.__base64_encoded = value

    @property
    def compress(self):
        return self.__compress

    @compress.setter
    def compress(self, value):
        self.__compress = value

    @property
    def code(self):
        if isinstance(self.__body, dict) and self.__code == 200 and not self.__body:
            return 204
        if isinstance(self.__body, dict) and self.__code == 200 and self.has_errors:
            return 400
        return self.__code

    @code.setter
    def code(self, code):
        self.__code = code

    @property
    def body(self):
        if self.compress:
            return self.__compress_body()
        if isinstance(self.__body, (dict, list, tuple)):
            return json.dumps(self.__body, use_decimal=True)
        return self.__body

    @body.setter
    def body(self, body):
        self.__body = body

    @property
    def response(self):
        body = self.body
        return {
            'isBase64Encoded': self.base64_encoded,
            'headers': self.headers,
            'statusCode': self.code,
            'body': body
        }

    @property
    def has_errors(self):
        return 'errors' in self.__body

    def set_error(self, key_path, message):
        error = {'key_path': key_path, 'message': message}
        if (isinstance(self.__body, dict) and 'errors' in self.__body):
            self.__body['errors'].append(error)
        else:
            self.__body = {'errors': [error]}

    def __compress_body(self):
        self.headers = ('Content-Encoding', 'gzip')
        self.base64_encoded = True
        compressed = BytesIO()
        body = json_helper.try_encode_json(self.__body)
        with gzip.GzipFile(fileobj=compressed, mode='w') as file:
            file.write(body.encode('utf-8'))
        return base64.b64encode(compressed.getvalue()).decode('ascii')

    def __str__(self):
        response = self.response
        return str({
            'has_errors': self.has_errors,
            'response': {
                'headers': response.get('headers', {}),
                'statusCode': response.get('statusCode', 200),
                'isBase64Encoded': response.get('isBase64Encoded', False),
                'body': json_helper.try_decode_json(response.get('body', {}))
            }
        })
