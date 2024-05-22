import copy
import os
import yaml


class OpenAPIGenerator:

    def __init__(self, output_location):
        file_location = self.__determine_if_openapi_exists(output_location)
        if file_location is not None:
            self.__doc_dict = self.__read_openapi(file_location)
        else:
            self.__doc_dict = self.__get_default_dict()
        self.__existing_path_methods = {}

    @property
    def doc(self):
        return self.__doc_dict

    def delete_unused_paths(self):
        doc_dict = copy.deepcopy(self.__doc_dict)
        for path in doc_dict['paths']:
            if path not in self.__existing_path_methods:
                del self.__doc_dict['paths'][path]
                continue
            for method in doc_dict['paths'][path]:
                if method not in self.__existing_path_methods[path]:
                    del self.__doc_dict['paths'][path][method]

    def add_path_and_method(self, module):
        route_method = self.__get_route_method(module)
        self.__set_route_method_tags(route_method, module)
        self.__set_operation_id(route_method, module)
        self.__set_deprecated(route_method, module)
        self.__set_security(route_method, module)
        self.__set_parameters(route_method, module)
        self.__set_request_body(route_method, module)
        self.__set_responses(route_method, module)
        self.__set_schemas(module)
        if module.route_path not in self.__existing_path_methods:
            self.__existing_path_methods[module.route_path] = []
        self.__existing_path_methods[module.route_path].append(module.method)

    def __get_route_method(self, module):
        paths = self.__doc_dict['paths']
        if not paths.get(module.route_path):
            paths[module.route_path] = {}
        route = paths[module.route_path]
        if not route.get(module.method):
            route[module.method] = {}
        return route[module.method]

    def __set_route_method_tags(self, route_method, module):
        if not route_method.get('tags'):
            route_method['tags'] = []
        route_method['tags'] = route_method['tags'] + module.tags
        route_method['tags'] = list(dict.fromkeys(route_method['tags']))

        route_tags = self.__add_doc_tag(route_method['tags'])
        doc_tags = self.__add_doc_tag(self.__doc_dict['tags'])
        combined_tags = route_tags + doc_tags
        self.__doc_dict['tags'] = [dict(tag) for tag in {tuple(combined_tag.items()) for combined_tag in combined_tags}]

    def __add_doc_tag(self, tags):
        doc_tags = []
        for tag in tags:
            if isinstance(tag, dict):
                doc_tags.append({'name': tag.get('name', 'AcaiGenerated')})
            else:
                doc_tags.append({'name': tag})
        return doc_tags

    def __set_operation_id(self, route_method, module):
        if not route_method.get('operationId'):
            route_method['operationId'] = module.operation_id

    def __set_deprecated(self, route_method, module):
        if not route_method.get('deprecated'):
            route_method['deprecated'] = False
        route_method['deprecated'] = module.deprecated

    def __set_security(self, route_method, module):
        if not route_method.get('security') and module.requires_auth:
            route_method['security'] = [{'AcaiGenerated': []}]

    def __set_parameters(self, route_method, module):
        route_method['parameters'] = []
        self.__set_param(route_method['parameters'], module.required_headers, 'header', True)
        self.__set_param(route_method['parameters'], module.available_headers, 'header', False)
        self.__set_param(route_method['parameters'], module.required_query, 'query', True)
        self.__set_param(route_method['parameters'], module.available_query, 'query', False)
        self.__set_param(route_method['parameters'], module.required_path_params, 'path', True)

    def __set_param(self, parameters, requirements, location, required):
        for requirement in requirements:
            parameters.append({
                'in': location,
                'name': requirement,
                'required': required,
                'schema': {
                    'type': 'string'
                }
            })

    def __set_request_body(self, route_method, module):
        if not route_method.get('requestBody') and module.request_body_schema:
            route_method['requestBody'] = {
                'required': True,
                'content': {
                    'application/json': {
                        'schema': {
                            '$ref': f'#/components/schemas/{module.request_body_schema_name}'
                        }
                    }
                }
            }

    def __set_responses(self, route_method, module):
        if module.response_body_schema:
            if not route_method.get('responses'):
                route_method['responses'] = {}
            route_method['responses']['200'] = {
                'description': 'OK',
                'content': {
                    'application/json': {
                        'schema': {
                            '$ref': f'#/components/schemas/{module.response_body_schema_name}'
                        }
                    }
                }
            }

    def __set_schemas(self, module):
        if module.request_body_schema:
            self.__doc_dict['components']['schemas'][module.request_body_schema_name] = module.request_body_schema
        if module.response_body_schema:
            self.__doc_dict['components']['schemas'][module.response_body_schema_name] = module.response_body_schema

    def __determine_if_openapi_exists(self, output_locaiton):
        file_locaiton = None
        if os.path.isfile(f'{output_locaiton}/openapi.yml'):
            file_locaiton = f'{output_locaiton}/openapi.yml'
        elif os.path.isfile(f'{output_locaiton}/openapi.json'):
            file_locaiton = f'{output_locaiton}/openapi.json'
        return file_locaiton

    def __read_openapi(self, file_location):
        with open(file_location, encoding='utf-8') as schema_file:
            return yaml.load(schema_file, Loader=yaml.FullLoader)

    def __get_default_dict(self):
        return {
            'openapi': '3.1.0',
            'info': {
                'version': '1.0.0',
                'title': 'Acai Generator',
                'license': {
                    'name': 'MIT'
                }
            },
            'tags': [],
            'servers': [],
            'paths': {},
            'components': {
                'securitySchemes': {
                    'AcaiGenerated': {
                        'type': 'apiKey',
                        'in': 'header',
                        'name': 'CHANGE-ME'
                    }
                },
                'schemas': {}
            }
        }
