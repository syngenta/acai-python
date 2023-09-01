from collections import OrderedDict


class ResolverCache:
    CACHE_ALL = 'all'
    CACHE_STATIC = 'static-only'
    CACHE_DYNAMIC = 'dynamic-only'

    def __init__(self, **kwargs):
        self.__cache = OrderedDict()
        self.__size = kwargs.get('cache_size', 128)
        self.__mode = kwargs.get('cache_mode', self.CACHE_ALL)

    def get(self, method_path):
        if method_path not in self.__cache:
            return {}
        self.__cache.move_to_end(method_path)
        return self.__cache[method_path]

    def put(self, route_path, endpoint, is_dynamic_route=False, dynamic_parts=None):
        if self.__size is None:
            return
        if is_dynamic_route and self.__mode == self.CACHE_STATIC:
            return
        if not is_dynamic_route and self.__mode == self.CACHE_DYNAMIC:
            return
        self.__cache[route_path] = {'endpoint': endpoint, 'is_dynamic_route': is_dynamic_route, 'dynamic_parts': dynamic_parts}
        self.__cache.move_to_end(route_path)
        if self.__size != 0 and len(self.__cache) > self.__size:
            self.__cache.popitem(last=False)
