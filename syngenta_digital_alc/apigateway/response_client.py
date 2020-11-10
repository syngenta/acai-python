import simplejson as json

from syngenta_digital_alc.common import json_helper

 
class ResponseClient:

    def __init__(self):
        self._body = {}
        self._code = 200
        self._headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': '*'
        }

    @property
    def headers(self):
        return self._headers

    @headers.setter
    def headers(self, key, value):
        self._headers[key] = value

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
        if (
            isinstance(self._body, dict)
            or isinstance(self._body, list)
            or isinstance(self._body, tuple)
        ):
            return json.dumps(self._body)
        return self._body

    @body.setter
    def body(self, body):
        self._body = body

    @property
    def response(self):
        return {
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
            self._body = {"errors": [error]}

    def __str__(self):
        response = self.response
        return str({
            'response': {
                'headers': response.get('headers', {}),
                'statusCode': response.get('statusCode', {}),
                'body': json_helper.try_decode_json(response.get('body', {}))
            },
            'has_errors': self.has_errors
        })
