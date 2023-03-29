import unittest
import logging

from acai.apigateway.cacher import Cacher
from acai.apigateway.endpoint import Endpoint
from acai.apigateway.importer import Importer


class CacherTest(unittest.TestCase):
    handler_path = 'tests/mocks/cacher/directory_handlers'

    def setUp(self):
        self.importer = Importer(handlers=self.handler_path, mode='directory')

    def test_cache_settings(self):
        cacher = Cacher()
        self.assertTrue(cacher.CACHE_ALL == 'all')
        self.assertTrue(cacher.CACHE_STATIC == 'static-only')
        self.assertTrue(cacher.CACHE_DYNAMIC == 'dynamic-only')

    def test_cache_put(self):
        file_path = f'/{self.importer.handlers_path_abs}/basic.py'
        import_path = 'tests.mocks.cacher.directory_handlers.basic'
        endpoint_module = self.importer.import_module_from_file(file_path, import_path)
        endpoint = Endpoint(endpoint_module, 'post')
        cacher = Cacher()
        try:
            cacher.put('post::/unit-test/v1/cacher/basic', endpoint)
            self.assertTrue(True)
        except Exception as exception:
            logging.exception(exception)
            self.assertTrue(False)

    def test_cache_put_and_get(self):
        file_path = f'/{self.importer.handlers_path_abs}/basic.py'
        import_path = 'tests.mocks.cacher.directory_handlers.basic'
        endpoint_module = self.importer.import_module_from_file(file_path, import_path)
        endpoint = Endpoint(endpoint_module, 'patch')
        cacher = Cacher()
        cacher.put('patch::/unit-test/v1/cacher/basic', endpoint)
        cached_endpoint = cacher.get('patch::/unit-test/v1/cacher/basic')
        self.assertTrue(cached_endpoint.has_requirements)

    def test_cache_get_miss(self):
        cacher = Cacher()
        endpoint = cacher.get('get::/unit-test/v1/cacher/basic')
        self.assertTrue(endpoint is None)

    def test_cache_lru_sequence_size_reaches_capacity_and_result_in_miss(self):
        file_path = f'/{self.importer.handlers_path_abs}/basic.py'
        import_path = 'tests.mocks.cacher.directory_handlers.basic'
        endpoint_module = self.importer.import_module_from_file(file_path, import_path)
        post_endpoint = Endpoint(endpoint_module, 'post')
        patch_endpoint = Endpoint(endpoint_module, 'patch')
        get_endpoint = Endpoint(endpoint_module, 'get')
        cacher = Cacher(cache_size=1)
        cacher.put('get::/unit-test/v1/cacher/basic', get_endpoint)
        get_cache_result = cacher.get('get::/unit-test/v1/cacher/basic')
        self.assertFalse(get_cache_result.has_requirements)
        cacher.put('patch::/unit-test/v1/cacher/basic', patch_endpoint)
        cacher.get('patch::/unit-test/v1/cacher/basic')
        cacher.put('post::/unit-test/v1/cacher/basic', post_endpoint)
        cacher.get('post::/unit-test/v1/cacher/basic')
        miss_cache_result = cacher.get('get::/unit-test/v1/cacher/basic')
        self.assertTrue(miss_cache_result is None)

    def test_cache_size_none_always_miss(self):
        file_path = f'/{self.importer.handlers_path_abs}/basic.py'
        import_path = 'tests.mocks.cacher.directory_handlers.basic'
        endpoint_module = self.importer.import_module_from_file(file_path, import_path)
        get_endpoint = Endpoint(endpoint_module, 'get')
        cacher = Cacher(cache_size=None)
        cacher.put('get::/unit-test/v1/cacher/basic', get_endpoint)
        get_cache_result = cacher.get('get::/unit-test/v1/cacher/basic')
        self.assertTrue(get_cache_result is None)

    def test_cache_static_only(self):
        file_path = f'/{self.importer.handlers_path_abs}/basic.py'
        import_path = 'tests.mocks.cacher.directory_handlers.basic'
        endpoint_module = self.importer.import_module_from_file(file_path, import_path)
        get_endpoint = Endpoint(endpoint_module, 'get')
        cacher = Cacher(cache_mode='static-only')
        cacher.put('get::/unit-test/v1/cacher/basic', get_endpoint)
        get_cache_result = cacher.get('get::/unit-test/v1/cacher/basic')
        self.assertFalse(get_cache_result.has_requirements)
        patch_endpoint = Endpoint(endpoint_module, 'patch')
        patch_endpoint.is_dynamic = True
        cacher.put('patch::/unit-test/v1/cacher/basic', patch_endpoint)
        patch_cache_result = cacher.get('patch::/unit-test/v1/cacher/basic')
        self.assertTrue(patch_cache_result is None)

    def test_cache_dynamic_only(self):
        file_path = f'/{self.importer.handlers_path_abs}/basic.py'
        import_path = 'tests.mocks.cacher.directory_handlers.basic'
        endpoint_module = self.importer.import_module_from_file(file_path, import_path)
        get_endpoint = Endpoint(endpoint_module, 'get')
        cacher = Cacher(cache_mode='dynamic-only')
        patch_endpoint = Endpoint(endpoint_module, 'patch')
        patch_endpoint.is_dynamic = True
        cacher.put('patch::/unit-test/v1/cacher/basic', patch_endpoint)
        patch_cache_result = cacher.get('patch::/unit-test/v1/cacher/basic')
        self.assertTrue(patch_cache_result.has_requirements)
        cacher.put('get::/unit-test/v1/cacher/basic', get_endpoint)
        get_cache_result = cacher.get('get::/unit-test/v1/cacher/basic')
        self.assertTrue(get_cache_result is None)
