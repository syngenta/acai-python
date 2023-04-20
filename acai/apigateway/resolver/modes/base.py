import abc

from acai.apigateway.resolver.importer import ResolverImporter


class BaseModeResolver(abc.ABC):

    def __init__(self, **kwargs):
        self.importer = ResolverImporter(handlers=kwargs['handlers'])
        self.has_dynamic_route = False
        self.dynamic_parts = {}
        self.base_path = self.importer.clean_path(kwargs['base_path'])

    def get_endpoint_module(self, request):
        file_path, import_path = self._get_file_and_import_path(request.path)
        return self.importer.import_module_from_file(file_path, import_path)

    def get_request_path_as_list(self, request_path):
        base_path = request_path.replace(self.base_path, '').replace('-', '_')
        clean_base = self.importer.clean_path(base_path)
        return clean_base.split('/')

    def get_abs_file_path(self, relative_file_path):
        return f'{self.importer.file_separator}'.join(['', self.importer.project_root, relative_file_path])

    def get_abs_import_path(self, relative_file_path):
        return relative_file_path.replace(self.importer.file_separator, '.').replace('.py', '')

    @abc.abstractmethod
    def _get_file_and_import_path(self, request_path):
        raise NotImplementedError
