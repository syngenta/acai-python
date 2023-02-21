from acai.apigateway.importer import Importer


class Directory:

    def __init__(self, **kwargs):  # pylint: disable=W0238
        self.__base_path = Importer.clean_path(kwargs['base_path'])
        self.__importer = Importer(handlers=kwargs['handler_path'], mode='directory')

    def resolve(self, request):  # pylint: disable=unused-argument
        handler_paths = self.__importer.list_files_in_handler_path()
        return handler_paths
