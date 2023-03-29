from acai.apigateway.resolver.modes.base import BaseModeResolver
from acai.apigateway.resolver.importer import ResolverImporter
from acai.apigateway.exception import ApiException


class MappingModeResolver(BaseModeResolver):

    def __init__(self, **kwargs):
        self.__handler_mapping = kwargs['handler_mapping']
        kwargs['handlers'] = '/'
        kwargs['routing_mode'] = 'mapping'
        super().__init__(**kwargs)

    def _get_file_and_import_path(self, request_path):
        path_list = self.__get_request_path_as_list(request_path)
        mapping_path_key = self.__get_matching_path_from_mapping(path_list)
        clean_path_key = self.__clean_mapping_key(mapping_path_key)
        mapping_file_path = self.__handler_mapping.get(clean_path_key)
        if mapping_file_path is None:
            raise ApiException(code=404, message='route not found')
        file_path = self.__get_abs_file_path(mapping_file_path)
        import_path = self.importer.clean_path(mapping_file_path).replace(self.importer.file_separator, '.').replace('.py', '')
        return file_path, import_path

    def __clean_mapping_key(self, mapping_path_key):
        base_path = [mapping_key for mapping_key in self.__handler_mapping if self.base_path in mapping_key]
        if base_path:
            mapping_path_key = f'{self.base_path}/{mapping_path_key}'
        slashes = [mapping_key for mapping_key in self.__handler_mapping if mapping_key.startswith('/')]
        if slashes:
            mapping_path_key = f'/{mapping_path_key}'
        return mapping_path_key

    def __get_abs_file_path(self, mapping_file_path):
        clean_path = self.importer.clean_path(mapping_file_path)
        base_dir = clean_path.split(self.importer.file_separator)[0]
        project_root = self.importer.project_root.split(base_dir)[0]
        join_list = ['', self.importer.clean_path(project_root), self.importer.clean_path(mapping_file_path)]
        return f'{self.importer.file_separator}'.join(join_list)

    def __get_request_path_as_list(self, request_path):
        base_path = request_path.replace(self.base_path, '')
        clean_base = self.importer.clean_path(base_path)
        return clean_base.split('/')

    def __get_matching_path_from_mapping(self, path_list):
        init_matching = list(self.__handler_mapping.keys())
        matching_path = self.__match_path_with_mapping(init_matching, path_list, 0)
        if len(matching_path) != 1 or len(matching_path) != len(path_list):
            raise ApiException(code=404, message='route not found')
        return f'{self.importer.file_separator}'.join(matching_path)

    def __match_path_with_mapping(self, routes, path_list, path_index):
        if path_index >= len(path_list) or not routes:
            return routes
        matching = []
        for route in routes:
            clean_route = self.__clean_route_mapping(route)
            if clean_route == path_list[path_index]:
                matching.append(clean_route)
        return self.__match_path_with_mapping(matching, path_list, path_index+1)

    def __clean_route_mapping(self, route):
        mapping_key = route.replace(self.base_path, '')
        return self.importer.clean_path(mapping_key)
