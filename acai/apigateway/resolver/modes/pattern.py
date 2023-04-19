from acai.apigateway.resolver.modes.base import BaseModeResolver
from acai.apigateway.exception import ApiException


class PatternModeResolver(BaseModeResolver):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__handler_pattern = kwargs['handlers']

    def _get_file_and_import_path(self, request_path):
        split_path = self.get_request_path_as_list(request_path)
        relative_path = self.__get_relative_path(split_path)
        relative_file_path = self.__handler_pattern.split(f'{self.importer.file_separator}*')[0] + self.importer.file_separator + relative_path
        file_path = self.get_abs_file_path(relative_file_path)
        import_path = self.get_abs_import_path(relative_file_path)
        return file_path, import_path

    def __get_relative_path(self, split_path):
        file_tree = self.importer.handlers_file_tree
        file_pattern = self.__get_file_pattern()
        relative_path = self.__get_import_path_file_tree(split_path, 0, file_tree, [], file_pattern)
        return f'{self.importer.file_separator}'.join(relative_path)

    def __get_file_pattern(self):
        split_pattern = self.__handler_pattern.split(self.importer.file_separator)
        file_pattern = split_pattern[-1]
        return file_pattern

    def __get_import_path_file_tree(self, split_path, split_index, file_tree, import_path, file_pattern):
        if split_index < len(split_path) and file_tree != '*':
            import_part = None
            route_part = split_path[split_index].replace("-", "_")
            mvvm = f'{route_part}'
            mvc = file_pattern.replace('*', route_part)
            if mvvm in file_tree:
                import_part = mvvm
                split_index = split_index - 1 if split_index + 1 == len(split_path) else split_index
            elif mvc in file_tree:
                import_part = mvc
            elif file_tree.get('__dynamic_files') and file_tree['__dynamic_files']:
                import_part = list(file_tree['__dynamic_files'])[0]
                self.has_dynamic_route = True
                self.dynamic_parts[split_index] = split_path[split_index]
            if import_part is not None:
                import_path.append(import_part)
                self.__get_import_path_file_tree(split_path, split_index+1, file_tree[import_part], import_path, file_pattern)
            else:
                raise ApiException(code=404, message='route not found')
        return import_path
