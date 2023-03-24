import copy
import os
import json

import jsonref
import yaml


class Schema:

    def __init__(self, **kwargs):
        self.__schema = kwargs.get('schema')
        self.__config = kwargs.get('schema_config', {})
        self.__spec = {}

    @property
    def spec(self):
        return self.__spec

    def get_openapi_spec(self):
        return self.__get_full_spec()

    def get_body_spec(self, required_body=None):
        if self.__schema and isinstance(self.__schema, dict):
            return self.__schema
        if required_body and isinstance(required_body, dict):
            return required_body
        return self.__get_component_spec(required_body)

    def get_route_spec(self, route, method):
        return self.__get_route_spec(route, method)

    def __get_full_spec(self):
        if not self.spec:
            unresolved_spec = self.__get_spec_from_file()
            resolved_spec = jsonref.loads(json.dumps(unresolved_spec), jsonschema=True, merge_props=True)
            self.__spec = self.__combine_all_of_spec(resolved_spec)
        return self.spec

    def __get_spec_from_file(self):
        abs_schema_path = self.__get_abs_spec_path()
        with open(abs_schema_path, encoding='utf-8') as schema_file:
            return yaml.load(schema_file, Loader=yaml.FullLoader)

    def __get_abs_spec_path(self):
        path = os.path.normpath(self.__schema)
        schema_root = path.split(os.sep)[0]
        dirty_root_path = os.getcwd().split(schema_root)[0]
        clean_root_path = dirty_root_path.strip(os.sep)
        asb_schema_path = f'{os.sep}' + clean_root_path + f'{os.sep}' + self.__schema.strip(os.sep)
        return asb_schema_path

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
        combined = {}
        for all_of in spec[spec_key]:
            if isinstance(all_of, dict):
                combined.update(all_of)
        if combined:
            del combined_spec['allOf']
            combined_spec.update(combined)

    def __iter_spec_list(self, spec, spec_key, combined_spec):
        for index, item in enumerate(spec[spec_key]):
            if isinstance(item, dict):
                self.__walk_spec(item, combined_spec[spec_key][index])

    def __get_component_spec(self, required_body=None):
        if not required_body:
            return {}
        spec = self.__get_full_spec()
        definition = spec['components']['schemas'][required_body]
        definition['additionalProperties'] = self.__config.get('allow_additional_properties', False)
        return definition

    def __get_route_spec(self, route, method):
        spec = self.__get_full_spec()
        if route[0] != '/':
            route = f'/{route}'
        if spec.get('basePath'):
            route = route.replace(spec['basePath'], '')
        return spec['paths'][route][method]
