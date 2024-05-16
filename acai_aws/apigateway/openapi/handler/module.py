import os

from pydantic import BaseModel


class HandlerModule:
    def __init__(self, handler_base, file_path, module, method, base):
        self.__handler_base = handler_base
        self.__file_path = file_path
        self.__module = module
        self.__method = method
        self.__base_path = base.strip(os.sep)
        self.__func = getattr(module, method)
        self.__requirements = getattr(self.__func, 'requirements', {})
        self.__route_path = ''

    @property
    def file_path(self):
        return self.__file_path

    @property
    def module(self):
        return self.__module

    @property
    def method(self):
        return self.__method.lower()

    @property
    def operation_id(self):
        id_prefix = ''.join(r for r in self.route_path.title() if r.isalnum())
        return f'{self.method.title()}{id_prefix}AcaiGenerated'

    @property
    def route_path(self):
        if self.__requirements.get('required_route'):
            self.__route_path = self.__requirements['required_route']
        if not self.__route_path:
            self.__route_path = self.__compose_route_path()
        return self.__route_path if self.__route_path.startswith('/') else f'/{self.__route_path}'
    
    @property
    def deprecated(self):
        return bool(self.__requirements.get('deprecated'))
    
    @property
    def summary(self):
        return self.__requirements.get('summary')
    
    @property
    def tags(self):
        return [self.__base_path.replace(os.sep, '-')]

    @property
    def requires_auth(self):
        return self.__requirements.get('auth_required')

    @property
    def required_headers(self):
        return self.__requirements.get('required_headers', [])

    @property
    def available_headers(self):
        return self.__requirements.get('available_headers', [])

    @property
    def required_query(self):
        return self.__requirements.get('required_query', [])

    @property
    def available_query(self):
        return self.__requirements.get('available_query', [])

    @property
    def required_path_params(self):
        path_params = []
        for path_part in self.route_path.split('/'):
            if '{' in path_part and '}' in path_part:
                cleaned_part = path_part.replace('{', '').replace('}', '')
                path_params.append(cleaned_part)
        return path_params

    @property
    def request_body_schema_name(self):
        return f'{self.method}{self.route_path.replace("/", "-").replace("_", "-").replace("{", "").replace("}", "")}-request-body'

    @property
    def request_body_schema(self):
        return self.__get_schema_body('required_body')

    @property
    def response_body_schema_name(self):
        return f'{self.method}{self.route_path.replace("/", "-").replace("_", "-").replace("{", "").replace("}", "")}-response-body'

    @property
    def response_body_schema(self):
        return self.__get_schema_body('required_response')

    def __compose_route_path(self):
        dirty_route = self.__file_path.split(self.__handler_base)[1]
        no_py_route = dirty_route.replace('.py', '')
        no_init_route = no_py_route.replace('__init__', '')
        clean_route = [self.__base_path]
        for route in no_init_route.split(os.sep):
            if route.startswith('_'):
                route = ''.join(route.split('_')[1])
                route = f'{{{route}}}'
            if route:
                clean_route.append(route)
        return '/'.join(clean_route)

    def __get_schema_body(self, schema_key):
        schema_body = self.__requirements.get(schema_key)
        if not schema_body or isinstance(schema_body, str):
            return None
        elif isinstance(schema_body, dict):
            return schema_body
        elif issubclass(schema_body, BaseModel):
            return schema_body.model_json_schema()
