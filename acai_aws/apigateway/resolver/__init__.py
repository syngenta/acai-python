from acai_aws.apigateway.resolver.cache import ResolverCache
from acai_aws.apigateway.endpoint import Endpoint
from acai_aws.apigateway.exception import ApiException
from acai_aws.apigateway.resolver.modes.directory import DirectoryModeResolver
from acai_aws.apigateway.resolver.modes.mapping import MappingModeResolver
from acai_aws.apigateway.resolver.modes.pattern import PatternModeResolver


class Resolver:
    PATTERN_MODE = 'pattern'
    DIRECTORY_MODE = 'directory'
    MAPPING_MODE = 'mapping'
    __cache_misses = 0
    __available_resolvers = {
        'directory': DirectoryModeResolver,
        'mapping': MappingModeResolver,
        'pattern': PatternModeResolver
    }

    def __init__(self, **kwargs):
        self.__mode = self.__determine_routing_mode(kwargs)
        self.__cacher = ResolverCache(**kwargs)
        self.__resolver = self.__available_resolvers[self.__mode](**kwargs)

    @property
    def cache_misses(self):
        return self.__cache_misses

    def auto_load(self):
        if self.__mode != self.MAPPING_MODE:
            self.__resolver.load_importer_files()

    def get_endpoint(self, request):
        endpoint_module = self.__get_endpoint_module(request)
        if not hasattr(endpoint_module, request.method):
            raise ApiException(code=403, message='method not allowed')
        endpoint = Endpoint(endpoint_module, request.method)
        self.__assign_normalized_route(request, endpoint)
        self.__check_dynamic_route_and_apply_params(request, endpoint)
        self.__cacher.put(request.path, endpoint_module,self.__resolver.has_dynamic_route, self.__resolver.dynamic_parts)
        self.__resolver.reset()
        return endpoint

    def __determine_routing_mode(self, kwargs):
        if isinstance(kwargs['handlers'], dict):
            return self.MAPPING_MODE
        if isinstance(kwargs['handlers'], str) and '*' in kwargs['handlers'] and '.py' in kwargs['handlers']:
            return self.PATTERN_MODE
        return self.DIRECTORY_MODE

    def __get_endpoint_module(self, request):
        cached = self.__cacher.get(request.path)
        endpoint_module = cached.get('endpoint')
        self.__resolver.has_dynamic_route = cached.get('is_dynamic_route', self.__resolver.has_dynamic_route)
        self.__resolver.dynamic_parts = cached.get('dynamic_parts', self.__resolver.dynamic_parts)
        if endpoint_module is None:
            self.__cache_misses += 1
            endpoint_module = self.__resolver.get_endpoint_module(request)
        return endpoint_module

    def __assign_normalized_route(self, request, endpoint):
        base_path_parts = self.__resolver.base_path.split('/')
        dirty_route_parts = endpoint.required_route.split('/') if endpoint.has_required_route else request.path.split('/')
        route_parts = [part for part in dirty_route_parts if part]
        combined_route = base_path_parts + route_parts
        final_route = list(dict.fromkeys(combined_route))
        request.route = '/'.join(final_route)

    def __check_dynamic_route_and_apply_params(self, request, endpoint):
        if not self.__resolver.has_dynamic_route:
            return
        if self.__resolver.has_dynamic_route and not endpoint.has_required_route:
            raise ApiException(
                code=404, 
                key_path=request.path, 
                message='no route found; endpoint does have required_route configured'
            )
        clean_request_path = [rp for rp in request.path.split('/') if rp and rp not in self.__resolver.base_path.split('/')]
        clean_endpoint_route = [er for er in endpoint.required_route.split('/') if er and er not in self.__resolver.base_path.split('/')]
        self.__check_dynamic_route(request, clean_request_path, clean_endpoint_route)
        self.__apply_dynamic_route_params(request, clean_endpoint_route)

    def __check_dynamic_route(self, request, clean_request_path, clean_endpoint_route):
        for index, _ in enumerate(clean_request_path):
            if clean_request_path[index] != clean_endpoint_route[index] and index not in list(self.__resolver.dynamic_parts.keys()):
                raise ApiException(
                    code=404, 
                    key_path=request.path, 
                    message='no route found; requested dynamic route does not match endpoint route definition'
                )

    def __apply_dynamic_route_params(self, request, required_route_parts):
        for part in list(self.__resolver.dynamic_parts.keys()):
            variable_name = required_route_parts[part]
            if not variable_name.startswith('{') or not variable_name.endswith('}'):
                raise ApiException(
                    code=404, 
                    key_path=request.path,
                    message='no route found; endpoint does not have proper variables in required_route'
                )
            dynamic_name = variable_name.strip('{').strip('}')
            request.path_params = dynamic_name, self.__resolver.dynamic_parts[part]
