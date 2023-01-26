import simplejson as json


class JsonHelper:

    @staticmethod
    def decode(data, raise_error=False):
        try:
            return json.loads(data, use_decimal=True)
        except Exception as error:
            if raise_error:
                raise error
            return data

    @staticmethod
    def encode(data, raise_error=False):
        try:
            return json.dumps(data, use_decimal=True)
        except Exception as error:
            if raise_error:
                raise error
            return data
