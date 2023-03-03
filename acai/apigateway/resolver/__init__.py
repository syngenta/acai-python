from acai.apigateway.endpoint import Endpoint
from acai.apigateway.exception import ApiException
from acai.apigateway.resolver.directory import Directory
from acai.apigateway.resolver.mapping import Mapping
from acai.apigateway.resolver.pattern import Pattern


class Resolver:
    __available_resolvers = {
        'directory': Directory,
        'mapping': Mapping,
        'pattern': Pattern
    }

    def __init__(self, **kwargs):
        self.__kwargs = kwargs
        self.__validate_config()
        self.__resolver_type = self.__available_resolvers[kwargs['routing_mode']](**kwargs)

    def get_endpoint(self, request):
        endpoint_module = self.__resolver_type.get_endpoint_module(request)
        if not hasattr(endpoint_module, request.method):
            raise ApiException(code=403, message='method not allowed')
        return Endpoint(endpoint_module, request.method)

    def __validate_config(self):
        if not self.__kwargs.get('base_path'):
            raise ApiException(code=500, message='base_path is required')
        if not self.__kwargs.get('routing_mode'):
            raise ApiException(code=500, message='routing_mode is required; must be one of `directory` || `pattern` || `mapping`')
        if self.__kwargs['routing_mode'] not in {'directory', 'pattern', 'mapping'}:
            raise ApiException(code=500, message='routing_mode must be one of `directory` || `pattern` || `mapping`')
        if self.__kwargs['routing_mode'] == 'directory' and not self.__kwargs.get('handler_path'):
            raise ApiException(code=500, message='`directory` routing_mode must use handler_path kwarg')
        if self.__kwargs['routing_mode'] == 'pattern' and not self.__kwargs.get('handler_pattern'):
            raise ApiException(code=500, message='`pattern` routing_mode must use handler_pattern kwarg')
        if self.__kwargs['routing_mode'] == 'mapping' and not self.__kwargs.get('handler_mapping'):
            raise ApiException(code=500, message='`mapping` routing_mode must use handler_mapping kwarg')
