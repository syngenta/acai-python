from acai_aws.apigateway.resolver.modes.base import BaseModeResolver
from acai_aws.apigateway.exception import ApiException


class DirectoryModeResolver(BaseModeResolver):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__handler_path = self.importer.clean_path(kwargs['handlers'])

    def _get_file_and_import_path(self, request_path):
        split_path = self.get_request_path_as_list(request_path)
        route_path = self.__get_route_path(split_path)
        file_path = self.__handler_path + self.importer.file_separator + route_path
        import_path = self.get_import_path(file_path)
        return file_path, import_path

    def __get_route_path(self, split_path):
        file_tree = self.importer.get_handlers_file_tree()
        self.__get_import_path_file_tree(split_path, 0, file_tree)
        return f'{self.importer.file_separator}'.join(self.import_path)

    def __get_import_path_file_tree(self, split_path, split_index, file_tree):
        if split_index < len(split_path):
            part = split_path[split_index]
            possible_directory = part.replace('-', '_')
            possible_file = f'{possible_directory}.py'
            if possible_directory in file_tree:
                self.__handle_directory_path_part(possible_directory, split_path, split_index, file_tree)
            elif possible_file in file_tree:
                self.__handle_file_path_part(possible_file, split_path, split_index, file_tree)
            elif file_tree.get('__dynamic_files') and file_tree['__dynamic_files']:
                self.__handle_dynamic_path_part(split_path, split_index, file_tree)
            else:
                raise ApiException(code=404, message='route not found')

    def __handle_directory_path_part(self, possible_directory, split_path, split_index, file_tree):
        self.append_import_path(possible_directory)
        if split_index+1 < len(split_path):
            file_leaf = self.determine_which_file_leaf(file_tree, possible_directory)
            self.__get_import_path_file_tree(split_path, split_index+1, file_leaf)
        else:
            self.append_import_path('__init__.py')

    def __handle_file_path_part(self, possible_file, split_path, split_index, file_tree):
        self.append_import_path(possible_file)
        file_leaf = self.determine_which_file_leaf(file_tree, possible_file)
        self.__get_import_path_file_tree(split_path, split_index+1, file_leaf)

    def __handle_dynamic_path_part(self, split_path, split_index, file_tree):
        file_part = list(file_tree['__dynamic_files'])[0]
        self.append_import_path(file_part)
        if '.py' not in file_part and split_index+1 == len(split_path):
            self.append_import_path('__init__.py')
        file_leaf = self.determine_which_file_leaf(file_tree, file_part)
        self.has_dynamic_route = True
        self.dynamic_parts[split_index] = split_path[split_index]
        self.__get_import_path_file_tree(split_path, split_index+1, file_leaf)
