from .directory import Directory


class Resolver:
    __available_resolvers = {
        'directory': Directory
    }

    def __init__(self, **kwargs):
        self.__resolver_type = self.__available_resolvers[kwargs['routing_mode']](**kwargs)

    def get_endpoint(self, request):
        endpoint = self.__resolver_type.get_endpoint_module(request)
        print(endpoint)
