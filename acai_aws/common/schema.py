import copy
import json
import inspect

import jsonref
from pydantic import BaseModel
import yaml


class Schema:

    def __init__(self, **kwargs):
        self.__schema = kwargs.get('schema')
        self.__config = kwargs.get('schema_config', {})
        self.__spec = {}

    @property
    def spec(self):
        return self.__spec

    def load_schema_file(self):
        self.__get_full_spec()

    def get_openapi_spec(self):
        return self.__get_full_spec()

    def get_body_spec(self, required_body=None):
        if required_body and inspect.isclass(required_body) and issubclass(required_body, BaseModel):
            return required_body
        elif self.__schema and isinstance(self.__schema, dict):
            body_spec = self.__schema
        elif required_body and isinstance(required_body, dict):
            body_spec = required_body
        elif required_body and isinstance(required_body, str):
            body_spec = self.__get_component_spec(required_body)
        body_spec['additionalProperties'] = self.__config.get('allow_additional_properties', False)
        return body_spec
    
    def get_route_spec(self, route, method):
        return self.__get_route_spec(route, method)        

    def __get_full_spec(self):
        if not self.spec and self.__schema:
            unresolved_spec = self.__get_spec_from_file()
            resolved_spec = jsonref.loads(json.dumps(unresolved_spec), jsonschema=True, merge_props=True)
            self.__spec = self.__combine_all_of_spec(resolved_spec)
        return self.spec

    def __get_spec_from_file(self):
        with open(self.__schema, encoding='utf-8') as schema_file:
            return yaml.load(schema_file, Loader=yaml.FullLoader)    

    def __combine_all_of_spec(self, spec):
        combined = copy.deepcopy(spec)
        return self.__walk_spec(spec, combined)

    def __walk_spec(self, spec, combined_spec):
        for spec_key in spec:
            if spec_key == 'allOf':
                self.__combine_all_of(spec, spec_key, combined_spec)
            elif isinstance(spec[spec_key], dict):
                self.__walk_spec(spec[spec_key], combined_spec[spec_key])
            elif isinstance(spec[spec_key], list):
                self.__iter_spec_list(spec, spec_key, combined_spec)
        return combined_spec

    def __combine_all_of(self, spec, spec_key, combined_spec):
        combined = {
            'type': 'object',
            'properties': {},
            'required': []
        }
        for all_of in spec[spec_key]:
            if isinstance(all_of, dict) and all_of.get('properties'):
                combined['properties'].update(all_of['properties'])
            if isinstance(all_of, dict) and all_of.get('required'):
                combined['required'] += all_of['required']
        if combined['properties']:
            del combined_spec['allOf']
            combined_spec.update(combined)

    def __iter_spec_list(self, spec, spec_key, combined_spec):
        for index, item in enumerate(spec[spec_key]):
            if isinstance(item, dict):
                self.__walk_spec(item, combined_spec[spec_key][index])

    def __get_component_spec(self, required_body=None):
        spec = self.__get_full_spec()
        return spec['components']['schemas'][required_body]

    def __get_route_spec(self, route, method):
        spec = self.__get_full_spec()
        if spec.get('basePath'):
            route = route.replace(spec['basePath'], '')
        return spec['paths'][route][method]
