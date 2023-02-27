
from acai.apigateway.importer import Importer


class Directory:  # pylint: disable=unused-private-member

    def __init__(self, **kwargs):
        self.__importer = Importer(handlers=kwargs['handler_path'], mode='directory')
        self.__handler_path = self.__importer.clean_path(kwargs['handler_path'])
        self.__base_path = self.__importer.clean_path(kwargs['base_path'])

    def resolve(self, request):  # pylint: disable=unused-argument
        split_path = self.__get_split_request_path(request.path)
        relative_path = self.__get_relative_path(split_path)
        file_path = self.__handler_path + self.__importer.file_separator + relative_path + '.py'
        return file_path

    def __get_split_request_path(self, request_path):
        base_path = request_path.replace(self.__base_path, '')
        clean_base = self.__importer.clean_path(base_path)
        return clean_base.split('/')

    def __get_relative_path(self, split_path):
        file_tree = self.__importer.handlers_file_tree
        import_path = self.__climb_file_tree(split_path, 0, file_tree, [])
        return f'{self.__importer.file_separator}'.join(import_path)

    def __climb_file_tree(self, split_path, split_index, file_tree, import_path):
        if split_index < len(split_path) and file_tree != '*':
            part = split_path[split_index]
            possible_directory = part.replace('-', '_')
            possible_file = f'{possible_directory}.py'
            if possible_directory in file_tree:
                import_path.append(part)
                if split_index+1 < len(split_path):
                    self.__climb_file_tree(split_path, split_index+1, file_tree[possible_directory], import_path)
                else:
                    import_path.append('__init__')
            if possible_file in file_tree:
                import_path.append(part)
                self.__climb_file_tree(split_path, split_index+1, file_tree[possible_file], import_path)
        return import_path
