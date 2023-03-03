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
        Resolver.validate_config(kwargs)
        self.__resolver = self.__available_resolvers[kwargs['routing_mode']](**kwargs)

    def get_endpoint(self, request):
        endpoint_module = self.__resolver.get_endpoint_module(request)
        if not hasattr(endpoint_module, request.method):
            raise ApiException(code=403, message='method not allowed')
        endpoint = Endpoint(endpoint_module, request.method)
        self.__check_and_apply_dynamic_route(request, endpoint)
        return endpoint

    @staticmethod
    def validate_config(params):
        if not params.get('base_path'):
            raise ApiException(code=500, message='base_path is required')
        if not params.get('routing_mode'):
            raise ApiException(code=500, message='routing_mode is required; must be one of `directory` || `pattern` || `mapping`')
        if params['routing_mode'] not in {'directory', 'pattern', 'mapping'}:
            raise ApiException(code=500, message='routing_mode must be one of `directory` || `pattern` || `mapping`')
        if params['routing_mode'] == 'directory' and not params.get('handler_path'):
            raise ApiException(code=500, message='`directory` routing_mode must use handler_path kwarg')
        if params['routing_mode'] == 'pattern' and not params.get('handler_pattern'):
            raise ApiException(code=500, message='`pattern` routing_mode must use handler_pattern kwarg')
        if params['routing_mode'] == 'mapping' and not params.get('handler_mapping'):
            raise ApiException(code=500, message='`mapping` routing_mode must use handler_mapping kwarg')

    def __check_and_apply_dynamic_route(self, request, endpoint):
        if self.__resolver.has_dynamic_route and not endpoint.has_required_route:
            raise ApiException(code=404, key_path=request.path, message='no route found; endpoint does have required_route configured')
        dynamic_parts = self.__resolver.dynamic_parts
        required_route_parts = [part for part in endpoint.required_route.split('/') if part]
        for part in list(dynamic_parts.keys()):
            variable_name = required_route_parts[part]
            if not variable_name.startswith('{') and not variable_name.endswith('}'):
                raise ApiException(code=404, key_path=request.path, message='no route found; endpoint does not have proper variables in required_route')
            dynamic_name = variable_name.strip('{').strip('}')
            request.path_params = dynamic_name, dynamic_parts[part]
        request.route = endpoint.required_route
