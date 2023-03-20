import json
import jsonref
import os
import yaml


class SchemaFactory:

    def __init__(self, **kwargs):
        self.__schema = kwargs['schema']
        self.__config = kwargs.get('schema_config', {})
        self.__schema_dict = {}

    def get_schema(self, required_body=None):
        if isinstance(self.__schema, dict):
            self.__schema_dict = self.__schema
        if not self.__schema_dict:
            self.__schema_dict = self.__get_combined_schema_from_file(required_body)
        return self.__schema_dict

    def __get_combined_schema_from_file(self, required_body):
        combined_schema = {}
        schema_dict = self.__get_schema_dict_from_file()
        definitions = jsonref.loads(json.dumps(schema_dict))['components']['schemas']
        definition_schema = definitions[required_body]
        json_schemas = definition_schema['allOf'] if definition_schema.get('allOf') else [definition_schema]
        for json_schema in json_schemas:
            combined_schema.update(json_schema)
        combined_schema['additionalProperties'] = self.__config.get('allow_additional_properties', False)
        return combined_schema

    def __get_schema_dict_from_file(self):
        abs_schema_path = self.__get_abs_schema_path()
        with open(abs_schema_path) as schema_file:
            return yaml.load(schema_file, Loader=yaml.FullLoader)

    def __get_abs_schema_path(self):
        path = os.path.normpath(self.__schema)
        schema_root = path.split(os.sep)[0]
        dirty_root_path = os.getcwd().split(schema_root)[0]
        clean_root_path = dirty_root_path.strip(os.sep)
        asb_schema_path = f'{os.sep}' + clean_root_path + f'{os.sep}' + self.__schema.strip(os.sep)
        return asb_schema_path
