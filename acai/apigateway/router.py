from acai.apigateway.resolver import Resolver


class Router: # pylint: disable=unused-private-member

    def __init__(self, **kwargs):
        self.__before_all = kwargs.get('before_all')
        self.__after_all = kwargs.get('after_all')
        self.__with_auth = kwargs.get('with_auth')
        self.__on_error = kwargs.get('on_error')
        self.__resolver = Resolver.get_resolver(**kwargs)

    def route(self, event, context):
        pass
