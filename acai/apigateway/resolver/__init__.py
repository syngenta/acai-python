from acai.apigateway.resolver.directory import Directory
from acai.apigateway.exception import ApiException


class Resolver:
    __available_resolvers = {
        'directory': Directory
    }

    def __init__(self, **kwargs):
        self.__resolver_type = self.__available_resolvers[kwargs['routing_mode']](**kwargs)

    def get_endpoint(self, request):
        endpoint_module = self.__resolver_type.get_endpoint_module(request)
        if not hasattr(endpoint_module, request.method):
            raise ApiException(code=403, message='method not allowed')
        return endpoint_module
