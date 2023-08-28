import json
import jsonref
from jsonschema import Draft7Validator
import yaml


class RequestValidator:

    def __init__(self, request_client, response_client, schema_path = ''):
        self.request_client = request_client
        self.response_client = response_client
        self.schema_path = schema_path
        self._required_pairings = {
            'required_headers': 'headers',
            'available_headers': 'headers',
            'required_params': 'params',
            'available_params': 'params',
            'required_body': 'body'
        }

    def validate_request(self, **kwargs):
        event = self.request_client.request
        for required_kwarg, event_loc in self._required_pairings.items():
            if kwargs.get(required_kwarg) and event_loc == 'body' and self.schema_path:
                self._required_body(kwargs[required_kwarg], event.get(event_loc))
            elif kwargs.get(required_kwarg) and 'required' in required_kwarg:
                self._required_fields(kwargs[required_kwarg], event.get(event_loc), event_loc)
            elif kwargs.get(required_kwarg) and 'available' in required_kwarg:
                self._available_fields(kwargs[required_kwarg], event.get(event_loc), event_loc)

    def _required_fields(self, required, sent, list_name=''):
        sent_keys = []
        if isinstance(sent, dict) and len(sent.keys()) > 0:
            sent_keys = sent.keys()
        missing_fields = [value for value in required if value not in sent_keys]
        if len(required) > 0:
            for field in missing_fields:
                self.response_client.code = 400
                self.response_client.set_error(list_name, 'Please provide {} in {}'.format(field, list_name))

    def _available_fields(self, available, sent, list_name=''):
        if len(available) > 0:
            unavailable_fields = [value for value in sent if value not in available]
            for field in unavailable_fields:
                self.response_client.code = 400
                self.response_client.set_error(list_name, '{} is not an available {}'.format(field, list_name))

    def _required_body(self, schema, request_body):
        if not isinstance(request_body, dict):
            self.response_client.set_error('message', 'request body is not valid JSON')
        else:
            self._check_body_for_errors(schema, request_body)

    def _check_body_for_errors(self, schema, request):
        json_schema = self._get_combined_schema(schema)
        schema_validator = Draft7Validator(json_schema)
        for schema_error in sorted(schema_validator.iter_errors(request), key=str):
            self.response_client.set_error(self._get_error_path(schema_error), schema_error.message)

    def _get_combined_schema(self, schema):
        combined_schema = {}
        swagger = self._get_api_doc()
        definitions = jsonref.loads(json.dumps(swagger))['components']['schemas']
        definition_schema = definitions[schema]
        json_schemas = definition_schema['allOf'] if definition_schema.get('allOf') else [definition_schema]
        for json_schema in json_schemas:
            combined_schema.update(json_schema)
        combined_schema['additionalProperties'] = False
        return combined_schema

    def _get_error_path(self, error):
        path = '.'.join(str(path) for path in error.path)
        return path if path else 'root'

    def _get_api_doc(self):
        with open(self.schema_path) as api_doc:
            return yaml.load(api_doc, Loader=yaml.FullLoader)
