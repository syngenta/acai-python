from acai.apigateway.resolver.directory import Directory


class Resolver:

    def __init__(self, **kwargs):
        self.available_resolvers = {
            'directory': Directory
        }

    @classmethod
    def get_resolver(cls, **kwargs):
        mode = kwargs['routing_mode']
        resolver = cls(**kwargs)
        return resolver.available_resolvers[mode](**kwargs)

    def resolve_endpoint(self, request, response):
        pass
