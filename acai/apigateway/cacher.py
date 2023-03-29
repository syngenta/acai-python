from collections import OrderedDict


class Cacher:
    CACHE_ALL = 'all'
    CACHE_STATIC = 'static-only'
    CACHE_DYNAMIC = 'dynamic-only'

    def __init__(self, **kwargs):
        self.__cache = OrderedDict()
        self.__size = kwargs.get('cache_size', 128)
        self.__mode = kwargs.get('cache_mode', self.CACHE_ALL)

    def get(self, method_path):
        if method_path not in self.__cache:
            return None
        self.__cache.move_to_end(method_path)
        return self.__cache[method_path]

    def put(self, method_path, endpoint):
        if self.__size is None:
            return
        if endpoint.is_dynamic and self.__mode == self.CACHE_STATIC:
            return
        if not endpoint.is_dynamic and self.__mode == self.CACHE_DYNAMIC:
            return
        self.__cache[method_path] = endpoint
        self.__cache.move_to_end(method_path)
        if self.__size != 0 and len(self.__cache) > self.__size:
            self.__cache.popitem(last=False)
