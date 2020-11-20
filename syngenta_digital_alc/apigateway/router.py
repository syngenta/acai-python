import importlib.util
import os

from syngenta_digital_alc.apigateway.response_client import ResponseClient
from syngenta_digital_alc.common import logger


class Router:

    def __init__(self, **kwargs):
        self.event = kwargs['event']
        self.context = kwargs['context']
        self.handler_path = kwargs['handler_path']
        self.base_path = kwargs['base_path']
        self.schema_path = kwargs.get('schema_path')
        self.router_response = ResponseClient()

    def route(self):
        route_results = self._route_request()
        if self.router_response.has_errors:
            return self.router_response.response
        return route_results

    def _route_request(self):
        handler_module = self._run_route()
        if handler_module:
            return self._run_method(handler_module)
        return None

    def _run_route(self):
        import_path = self._get_import_path()
        file_path = self._get_file_path()
        if os.path.exists(file_path):
            spec = importlib.util.spec_from_file_location(import_path, file_path)
            handler_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(handler_module)
            return handler_module
        self._set_error(404, 'url', 'path not found')
        return None

    def _run_method(self, handler_module):
        method = self.event['httpMethod'].lower()
        if hasattr(handler_module, method):
            return self._run_endpoint(handler_module, method)
        self._set_error(403, 'method', 'method not allowed')
        return None

    def _run_endpoint(self, handler_module, method):
        try:
            method_results = getattr(handler_module, method)(self.event, self.context, self.schema_path)
            return method_results
        except Exception as error:
            self._set_error(500, 'server', 'internal server error', error)

    def _clean_path(self, path):
        if path[0] == '/':
            path = path[1:]
        if path[-1] == '/':
            path = path[:-1]
        return path

    def _get_import_path(self):
        event_path = self._clean_path(self.event['path'])
        base_path = self._clean_path(self.base_path)
        endpoint_import = event_path.replace('{}'.format(base_path), '').replace('-', '_')
        return '{}.{}'.format(self.handler_path, endpoint_import)

    def _get_file_path(self):
        event_path = self._clean_path(self.event['path'])
        base_path = self._clean_path(self.base_path)
        endpoint_file = event_path.replace('{}'.format(base_path), '').replace('-', '_')
        if not endpoint_file:
            endpoint_file = '__init__'
        return '{}/{}.py'.format(self.handler_path.replace('.', '/'), endpoint_file)

    def _set_error(self, code, key_path, message, error = None):
        self.router_response.code = code
        self.router_response.set_error(key_path, message)
        if error and not os.getenv('UNITTEST'):
            logger.log(level='ERROR', log=error, trace=True)
