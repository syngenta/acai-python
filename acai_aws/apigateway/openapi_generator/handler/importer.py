import importlib.util
import os

from acai_aws.apigateway.openapi_generator.handler.module import HandlerModule


class HandlerImporter:

    def get_modules_from_file_paths(self, file_paths):
        SUPPORTED_METHODS = ['any', 'delete', 'get', 'head', 'options', 'patch', 'post', 'put']
        modules = []
        for file_path in file_paths:
            try:
                import_path = self.__get_import_path_from_file(file_path)
                module = self.import_module_from_file(file_path, import_path)
                for method in dir(module):
                    if method.lower() in SUPPORTED_METHODS:
                        modules.append(HandlerModule(file_path, module, method))
            except:  # noqa: E722
                pass
        return modules
    
    def import_module_from_file(self, file_path, import_path):
        spec = importlib.util.spec_from_file_location(import_path, file_path)
        handler_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(handler_module)
        return handler_module
    
    def __get_import_path_from_file(self, file_path):
        return file_path.replace(os.sep, '.').replace('.py', '')