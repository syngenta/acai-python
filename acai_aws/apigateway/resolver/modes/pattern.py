from acai_aws.apigateway.resolver.modes.base import BaseModeResolver
from acai_aws.apigateway.exception import ApiException


class PatternModeResolver(BaseModeResolver):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__handler_pattern = kwargs['handlers']

    def _get_file_and_import_path(self, request_path):
        split_path = self.get_request_path_as_list(request_path)
        route_path = self.__get_relative_path(split_path)
        file_path = self.__handler_pattern.split(f'{self.importer.file_separator}*')[0] + self.importer.file_separator + route_path
        import_path = self.get_import_path(file_path)
        return file_path, import_path

    def __get_relative_path(self, split_path):
        file_tree = self.importer.get_handlers_file_tree()
        file_pattern = self.__get_file_pattern()
        self.__get_import_path_file_tree(split_path, 0, file_tree, file_pattern)
        return f'{self.importer.file_separator}'.join(self.import_path)

    def __get_file_pattern(self):
        split_pattern = self.__handler_pattern.split(self.importer.file_separator)
        file_pattern = split_pattern[-1]
        return file_pattern

    def __get_import_path_file_tree(self, split_path, split_index, file_tree, file_pattern):
        if split_index < len(split_path):
            import_part = None
            route_part = split_path[split_index].replace('-', '_')
            possible_directory = f'{route_part}'
            possible_file = file_pattern.replace('*', route_part)
            if possible_directory in file_tree:
                import_part = possible_directory
                split_index = split_index - 1 if split_index + 1 == len(split_path) else split_index
            elif possible_file in file_tree:
                import_part = possible_file
            elif file_tree.get('__dynamic_files') and file_tree['__dynamic_files']:
                import_part = list(file_tree['__dynamic_files'])[0]
                self.has_dynamic_route = True
                self.dynamic_parts[split_index] = split_path[split_index]
            if import_part is not None:
                self.append_import_path(import_part)
                file_leaf = self.determine_which_file_leaf(file_tree, import_part)
                index_file = file_pattern.replace('*', import_part)
                if '.py' not in import_part and split_index+1 == len(split_path) and index_file in file_leaf:
                    self.append_import_path(index_file)
                self.__get_import_path_file_tree(split_path, split_index+1, file_leaf, file_pattern)
            else:
                raise ApiException(code=404, message='route not found')
