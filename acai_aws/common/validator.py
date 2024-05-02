from collections import defaultdict

from jsonschema import Draft7Validator
from pydantic import BaseModel, ValidationError

from acai_aws.common.schema import Schema


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

    def auto_load(self):
        self.__schema.load_schema_file()

    def request_has_security(self, request):
        route_spec = self.__schema.get_route_spec(request.route, request.method)
        if route_spec.get('security'):
            return True
        return False

    def validate_request_with_openapi(self, request, response):
        route_spec = self.__schema.get_route_spec(request.route, request.method)
        requirements = Validator.combine_parameters(route_spec.get('parameters', []))
        if route_spec.get('requestBody'):
            requirements['required_body'] = route_spec['requestBody']['content'][request.content_type]['schema']
        self.validate_request(request, response, requirements)

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

    def validate_response_with_openapi(self, request, response):
        requirements = {}
        route_spec = self.__schema.get_route_spec(request.route, request.method)
        if route_spec.get('responses'):
            requirements['required_response'] = route_spec['responses'][f'{response.code}']['content'][response.content_type]['schema']
        self.validate_response(response, requirements)

    def validate_response(self, response, requirements):
        Validator.check_required_body(response, self.__schema.get_body_spec(requirements.get('required_response', {})), response.raw)
        if response.has_errors:
            response.set_error('response', 'There was a problem with the APIs response; does not match defined schema')
            response.code = 500

    def validate_record_body(self, body, schema):
        errors = []
        schema_validator = Draft7Validator(self.__schema.get_body_spec(schema))
        for schema_error in sorted(schema_validator.iter_errors(body), key=str):
            error_key = Validator.format_schema_error_key(schema_error)
            errors.append({'key': error_key, 'message': schema_error.message})
        return errors

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
        if not Validator.is_json(response, request_body):
            return False
        if schema and isinstance(schema, dict):
            schema_validator = Draft7Validator(schema)
            for schema_error in sorted(schema_validator.iter_errors(request_body), key=str):
                error_key = Validator.format_schema_error_key(schema_error)
                response.set_error(key_path=error_key, message=schema_error.message)
        elif issubclass(schema, BaseModel):
            try:
                schema(**request_body)
            except ValidationError as error:
                [response.set_error(key_path='.'.join(error['loc']), message=error['msg']) for error in error.errors()]

    @staticmethod
    def combine_parameters(parameters):
        requirements = defaultdict(lambda: [])
        for param in parameters:
            if param.get('in') == 'query' and param.get('required'):
                requirements['required_query'].append(param['name'])
            elif param.get('in') == 'query':
                requirements['available_query'].append(param['name'])
            elif param.get('in') == 'header' and param.get('required'):
                requirements['required_headers'].append(param['name'])
            elif param.get('in') == 'header':
                requirements['available_headers'].append(param['name'])
        return dict(requirements)

    @staticmethod
    def format_schema_error_key(schema_error):
        error_path = '.'.join(str(path) for path in schema_error.path)
        return error_path if error_path else 'root'

    @staticmethod
    def is_json(response, request_body):
        if not isinstance(request_body, dict):
            response.set_error('body', 'Expecting JSON request body; please make sure using proper content-type headers and body string is properly encoded')
            return False
        return True
