from acai.apigateway.resolver.modes.base import BaseModeResolver
from acai.apigateway.exception import ApiException


class MappingModeResolver(BaseModeResolver):

    def __init__(self, **kwargs):
        self.__handler_mapping = kwargs['handlers']
        kwargs['handlers'] = '/'
        super().__init__(**kwargs)

    def _get_file_and_import_path(self, request_path):
        path_list = self.__get_request_path_as_list(request_path)
        mapping_path_key = self.__get_matching_path_from_mapping(path_list)
        mapping_file_path = self.__try_get_mapping_file_path(mapping_path_key)
        if mapping_file_path is None:
            raise ApiException(code=404, message='route not found')
        file_path = self.__get_abs_file_path(mapping_file_path)
        import_path = self.importer.clean_path(mapping_file_path).replace(self.importer.file_separator, '.').replace('.py', '')
        return file_path, import_path

    def __try_get_mapping_file_path(self, mapping_path_key):
        mapping_file_path = self.__handler_mapping.get(mapping_path_key)
        if not mapping_file_path:
            mapping_file_path = self.__handler_mapping.get(f'{self.base_path}/{mapping_path_key}')
        if not mapping_file_path:
            mapping_file_path = self.__handler_mapping.get(f'/{mapping_path_key}')
        if not mapping_file_path:
            mapping_file_path = self.__handler_mapping.get(f'/{self.base_path}/{mapping_path_key}')
        return mapping_file_path

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
        mapping_keys = [self.__clean_route_mapping(route).split('/') for route in list(self.__handler_mapping.keys())]
        matching_path = self.__match_mapping_with_path(mapping_keys, path_list)
        if len(matching_path) != len(path_list):
            raise ApiException(code=404, message='route not found')
        return f'{self.importer.file_separator}'.join(matching_path)

    def __clean_route_mapping(self, route):
        mapping_key = route.replace(self.base_path, '')
        return self.importer.clean_path(mapping_key)

    def __match_mapping_with_path(self, mapping_list, path_list):
        for mapping in mapping_list:
            matching = self.__match_mapping(mapping, path_list)
            if matching:
                return matching
        return []

    def __match_mapping(self, route, path_list):
        matching = []
        if len(route) == len(path_list):
            for index, _ in enumerate(path_list):
                if path_list[index] == route[index] or route[index].startswith('{') and route[index].endswith('}'):
                    matching.append(route[index])
                else:
                    matching = []
        return matching
