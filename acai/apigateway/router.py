from acai.apigateway.resolver import Resolver


class Router:

    def __init__(self, **kwargs):  # pylint: disable=W0238
        self.__before_all = kwargs.get('before_all')
        self.__after_all = kwargs.get('after_all')
        self.__with_auth = kwargs.get('with_auth')
        self.__on_error = kwargs.get('on_error')
        self.__resolver = Resolver.get_resolver(**kwargs)

    def route(self, event, context):
        pass