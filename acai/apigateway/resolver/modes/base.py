import abc

from acai.apigateway.resolver.importer import ResolverImporter


class BaseModeResolver(abc.ABC):

    def __init__(self, **kwargs):
        self.importer = ResolverImporter(handlers=kwargs['handlers'], mode=kwargs['routing_mode'])
        self.has_dynamic_route = False
        self.dynamic_parts = {}
        self.base_path = self.importer.clean_path(kwargs['base_path'])

    def get_endpoint_module(self, request):
        file_path, import_path = self._get_file_and_import_path(request.path)
        return self.importer.import_module_from_file(file_path, import_path)

    @abc.abstractmethod
    def _get_file_and_import_path(self, request_path):
        raise NotImplementedError
