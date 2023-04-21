from acai.apigateway.resolver.modes.base import BaseModeResolver
from acai.apigateway.exception import ApiException


class DirectoryModeResolver(BaseModeResolver):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__handler_path = self.importer.clean_path(kwargs['handlers'])
        self.__file_tree_climbed = True
        self.__import_path = []

    def _get_file_and_import_path(self, request_path):
        split_path = self.get_request_path_as_list(request_path)
        relative_path = self.__get_relative_path(split_path)
        relative_file_path = self.__handler_path + self.importer.file_separator + relative_path
        abs_file_path = self.get_abs_file_path(relative_file_path)
        abs_import_path = self.get_abs_import_path(relative_file_path)
        return abs_file_path, abs_import_path

    def __get_relative_path(self, split_path):
        file_tree = self.importer.get_handlers_file_tree()
        self.__get_import_path_file_tree(split_path, 0, file_tree)
        return f'{self.importer.file_separator}'.join(self.__import_path)

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
        self.__append_import_path(possible_directory)
        if split_index+1 < len(split_path):
            file_leaf = self.__determine_which_file_leaf(file_tree, possible_directory)
            self.__get_import_path_file_tree(split_path, split_index+1, file_leaf)
        else:
            self.__append_import_path('__init__.py')

    def __handle_file_path_part(self, possible_file, split_path, split_index, file_tree):
        self.__append_import_path(possible_file)
        file_leaf = self.__determine_which_file_leaf(file_tree, possible_file)
        self.__get_import_path_file_tree(split_path, split_index+1, file_leaf)

    def __handle_dynamic_path_part(self, split_path, split_index, file_tree):
        file_part = list(file_tree['__dynamic_files'])[0]
        self.__append_import_path(file_part)
        if '.py' not in file_part and split_index+1 == len(split_path):
            self.__append_import_path('__init__.py')
        file_leaf = self.__determine_which_file_leaf(file_tree, file_part)
        self.has_dynamic_route = True
        self.dynamic_parts[split_index] = split_path[split_index]
        self.__get_import_path_file_tree(split_path, split_index+1, file_leaf)

    def __determine_which_file_leaf(self, file_tree, file_branch):
        if file_tree.get(file_branch) and file_tree[file_branch] != '*':
            self.__file_tree_climbed = True
            return file_tree[file_branch]
        self.__file_tree_climbed = False
        return file_tree

    def __append_import_path(self, path_part):
        if self.__file_tree_climbed:
            self.__import_path.append(path_part)
