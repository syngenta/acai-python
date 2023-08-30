import abc

from acai_aws.apigateway.resolver.importer import ResolverImporter


class BaseModeResolver(abc.ABC):

    def __init__(self, **kwargs):
        self.importer = ResolverImporter(handlers=kwargs['handlers'])
        self.base_path = self.importer.clean_path(kwargs['base_path'])
        self.has_dynamic_route = False
        self.file_tree_climbed = True
        self.dynamic_parts = {}
        self.import_path = []
    
    @abc.abstractmethod
    def _get_file_and_import_path(self, request_path):
        raise NotImplementedError

    def load_importer_files(self):
        self.importer.get_handlers_file_tree()

    def get_endpoint_module(self, request):
        file_path, import_path = self._get_file_and_import_path(request.path)
        return self.importer.import_module_from_file(file_path, import_path)

    def get_import_path(self, relative_file_path):
        return relative_file_path.replace(self.importer.file_separator, '.').replace('.py', '')

    def get_request_path_as_list(self, request_path):
        base_path = request_path.replace(self.base_path, '').replace('-', '_')
        clean_base = self.importer.clean_path(base_path)
        return clean_base.split('/')

    def determine_which_file_leaf(self, file_tree, file_branch):
        if file_tree.get(file_branch) and file_tree[file_branch] != '*':
            self.file_tree_climbed = True
            return file_tree[file_branch]
        self.file_tree_climbed = False
        return file_tree

    def append_import_path(self, path_part):
        if self.file_tree_climbed:
            self.import_path.append(path_part)

    def reset(self):
        self.has_dynamic_route = False
        self.dynamic_parts = {}
        self.file_tree_climbed = True
        self.import_path = []
