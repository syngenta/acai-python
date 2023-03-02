from .directory import Directory


class Resolver:  # pylint: disable=unused-private-member

    def __init__(self, **kwargs):
        self.__mode = kwargs['routing_mode']
        self.__available_resolvers = {
            'directory': Directory
        }
        self.__resolver_type = self.__available_resolvers[self.__mode](**kwargs)

    def resolve_endpoint(self, request, response):
        pass
