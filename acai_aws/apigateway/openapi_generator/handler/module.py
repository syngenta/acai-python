import os


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
        return self.__method

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
        return self.__route_path

    @property
    def requires_auth(self):
        return self.__requirements.get('auth_required')

    @property
    def required_headers(self):
        return self.__requirements.get('required_headers')

    @property
    def available_headers(self):
        return self.__requirements.get('available_headers')

    @property
    def required_query(self):
        return self.__requirements.get('required_query')

    @property
    def available_query(self):
        return self.__requirements.get('available_query')

    @property
    def request_body_shema_name(self): # need to generate unique schema name
        return self.__requirements.get('request_body')
    
    @property
    def request_body_shema(self): # need to determine schema body; if requirements is string return nothing
        return self.__requirements.get('request_body')

    @property
    def response_body_shema_name(self):
        return self.__requirements.get('required_response')

    @property
    def response_body_shema(self):
        return self.__requirements.get('required_response')

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