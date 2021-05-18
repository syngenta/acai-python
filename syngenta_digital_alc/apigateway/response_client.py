import simplejson as json

from syngenta_digital_alc.common import json_helper


class ResponseClient:

    def __init__(self):
        self._body = {}
        self._code = 200
        self._base64_encoded = False
        self._multi_value_headers = {}
        self._headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': '*'
        }

    @property
    def headers(self):
        return self._headers

    @headers.setter
    def headers(self, value):
        key, val = value
        self._headers[key] = val

    @property
    def base64_encoded(self):
        return self._base64_encoded

    @base64_encoded.setter
    def base64_encoded(self, value):
        self._base64_encoded = value

    @property
    def code(self):
        if isinstance(self._body, dict) and self._code == 200 and not self._body:
            return 204
        if isinstance(self._body, dict) and self._code == 200 and self.has_errors:
            return 400
        return self._code

    @code.setter
    def code(self, code):
        self._code = code

    @property
    def body(self):
        if isinstance(self._body, (dict, list, tuple)):
            return json.dumps(self._body, use_decimal=True)
        return self._body

    @body.setter
    def body(self, body):
        self._body = body

    @property
    def response(self):
        return {
            'isBase64Encoded': self.base64_encoded,
            'headers': self.headers,
            'statusCode': self.code,
            'body': self.body
        }

    @property
    def has_errors(self):
        return 'errors' in self._body

    def set_error(self, key_path, message):
        error = {'key_path': key_path, 'message': message}
        if (isinstance(self._body, dict) and 'errors' in self._body):
            self._body['errors'].append(error)
        else:
            self._body = {'errors': [error]}

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
