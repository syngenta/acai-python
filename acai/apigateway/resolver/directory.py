from acai.apigateway.importer import Importer
from acai.apigateway.resolver.exception import ResolverException


class Directory:

    def __init__(self, **kwargs):
        self.__importer = Importer(handlers=kwargs['handler_path'], mode='directory')
        self.__handler_path = self.__importer.clean_path(kwargs['handler_path'])
        self.__base_path = self.__importer.clean_path(kwargs['base_path'])

    def get_file_and_import_path(self, request):
        split_path = self.__get_request_path_as_list(request.path)
        relative_path = self.__get_relative_path(split_path)
        file_path = self.__handler_path + self.__importer.file_separator + relative_path
        import_path = file_path.replace(self.__importer.file_separator, '.').replace('.py', '')
        return file_path, import_path

    def __get_request_path_as_list(self, request_path):
        base_path = request_path.replace(self.__base_path, '').replace('-', '_')
        clean_base = self.__importer.clean_path(base_path)
        return clean_base.split('/')

    def __get_relative_path(self, split_path):
        file_tree = self.__importer.handlers_file_tree
        import_path = self.__get_import_path_file_tree(split_path, 0, file_tree, [])
        return f'{self.__importer.file_separator}'.join(import_path)

    def __get_import_path_file_tree(self, split_path, split_index, file_tree, import_path):
        if split_index < len(split_path) and file_tree != '*':
            part = split_path[split_index]
            possible_directory = part.replace('-', '_')
            possible_file = f'{possible_directory}.py'
            if possible_directory in file_tree:
                self.__handle_directory_path_part(import_path, possible_directory, split_path, split_index, file_tree)
            elif possible_file in file_tree:
                self.__handle_file_path_part(import_path, possible_file, split_path, split_index, file_tree)
            elif file_tree.get('__dynamic_files') and file_tree['__dynamic_files']:
                self.__handle_dynamic_path_part(import_path, split_path, split_index, file_tree)
            else:
                raise ResolverException(code=404, key_path='/'.join(split_path), message='route not found')
        return import_path

    def __handle_directory_path_part(self, import_path, possible_directory, split_path, split_index, file_tree):
        import_path.append(possible_directory)
        if split_index+1 < len(split_path):
            self.__get_import_path_file_tree(split_path, split_index+1, file_tree[possible_directory], import_path)
        else:
            import_path.append('__init__.py')

    def __handle_file_path_part(self, import_path, possible_file, split_path, split_index, file_tree):
        import_path.append(possible_file)
        self.__get_import_path_file_tree(split_path, split_index+1, file_tree[possible_file], import_path)

    def __handle_dynamic_path_part(self, import_path, split_path, split_index, file_tree):
        file_part = list(file_tree['__dynamic_files'])[0]
        import_path.append(file_part)
        self.__get_import_path_file_tree(split_path, split_index+1, file_tree[file_part], import_path)
