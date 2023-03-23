from jsonschema import Draft7Validator

from acai.common.schema import Schema


class Validator:

    def __init__(self, **kwargs):
        self.__schema = Schema(**kwargs)
        self.__pairings = {
            'required_headers': 'headers',
            'available_headers': 'headers',
            'required_query': 'query_params',
            'available_query': 'query_params',
            'required_body': 'body'
        }

    def validate_request_with_openapi(self, request, response):
        pass

    def validate_request(self, request, response, requirements):
        for required, source in self.__pairings.items():
            if requirements.get(required) and required == 'required_body':
                Validator.check_required_body(response, self.__schema.get_body_spec(requirements[required]), getattr(request, source))
            elif requirements.get(required) and 'required' in required:
                Validator.check_required_fields(response, requirements[required], getattr(request, source), source)
            elif requirements.get(required) and 'available' in required:
                full_list = Validator.combine_available_with_required(requirements, required)
                Validator.check_available_fields(response, full_list, getattr(request, source), source)
        if response.has_errors:
            response.code = 400

    @staticmethod
    def check_required_fields(response, required, sent, list_name=''):
        sent_keys = []
        if isinstance(sent, dict) and len(sent.keys()) > 0:
            sent_keys = sent.keys()
        missing_fields = [value for value in required if value not in sent_keys]
        if len(required) > 0:
            for field in missing_fields:
                response.set_error(list_name, f'Please provide {field} in {list_name}')

    @staticmethod
    def check_available_fields(response, available, sent, list_name=''):
        if len(available) > 0:
            unavailable_fields = [value for value in sent if value not in available]
            for field in unavailable_fields:
                response.set_error(list_name, f'{field} is not an available {list_name}')

    @staticmethod
    def combine_available_with_required(requirements, required):
        avail_list = requirements[required]
        if required == 'available_query' and requirements.get('required_query'):
            avail_list += requirements['required_query']
        elif required == 'available_headers' and requirements.get('required_headers'):
            avail_list += requirements['required_headers']
        return avail_list

    @staticmethod
    def check_required_body(response, schema, request_body):
        if schema:
            schema_validator = Draft7Validator(schema)
            for schema_error in sorted(schema_validator.iter_errors(request_body), key=str):
                error_path = '.'.join(str(path) for path in schema_error.path)
                error_key = error_path if error_path else 'root'
                response.set_error(key_path=error_key, message=schema_error.message)
