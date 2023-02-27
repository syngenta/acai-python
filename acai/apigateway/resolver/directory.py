from acai.apigateway.importer import Importer


class Directory: # pylint: disable=unused-private-member

    def __init__(self, **kwargs):
        self.__base_path = Importer.clean_path(kwargs['base_path'])
        self.__handler_path = kwargs['handler_path']
        self.__importer = Importer(handlers=self.__handler_path, mode='directory')

    def resolve(self, request):  # pylint: disable=unused-argument
        handler_paths = self.__importer.list_files_in_handler_path()
        return handler_paths
