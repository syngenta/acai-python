import unittest
import logging

from acai_aws.apigateway.resolver.cache import ResolverCache
from acai_aws.apigateway.endpoint import Endpoint
from acai_aws.apigateway.resolver.importer import ResolverImporter


class ResolverCacheTest(unittest.TestCase):
    handler_path = 'tests/mocks/apigateway/cacher/directory_handlers'

    def setUp(self):
        self.importer = ResolverImporter(handlers=self.handler_path, mode='directory')

    def test_cache_settings(self):
        cacher = ResolverCache()
        self.assertTrue(cacher.CACHE_ALL == 'all')
        self.assertTrue(cacher.CACHE_STATIC == 'static-only')
        self.assertTrue(cacher.CACHE_DYNAMIC == 'dynamic-only')

    def test_cache_put(self):
        file_path = f'{self.handler_path}/basic.py'
        import_path = 'tests.mocks.apigateway.cacher.directory_handlers.basic'
        endpoint_module = self.importer.import_module_from_file(file_path, import_path)
        endpoint = Endpoint(endpoint_module, 'post')
        cacher = ResolverCache()
        try:
            cacher.put('post::/unit-test/v1/cacher/basic', endpoint, False, {})
            self.assertTrue(True)
        except Exception as exception:
            logging.exception(exception)
            self.assertTrue(False)

    def test_cache_put_and_get(self):
        file_path = f'{self.handler_path}/basic.py'
        import_path = 'tests.mocks.apigateway.cacher.directory_handlers.basic'
        endpoint_module = self.importer.import_module_from_file(file_path, import_path)
        endpoint = Endpoint(endpoint_module, 'patch')
        cacher = ResolverCache()
        cacher.put('patch::/unit-test/v1/cacher/basic', endpoint, False, {})
        cached = cacher.get('patch::/unit-test/v1/cacher/basic')
        self.assertTrue(cached['endpoint'].has_requirements)

    def test_cache_get_miss(self):
        cacher = ResolverCache()
        cached = cacher.get('get::/unit-test/v1/cacher/basic')
        self.assertTrue(cached.get('endpoint') is None)

    def test_cache_lru_sequence_size_reaches_capacity_and_result_in_miss(self):
        file_path = f'{self.handler_path}/basic.py'
        import_path = 'tests.mocks.apigateway.cacher.directory_handlers.basic'
        endpoint_module = self.importer.import_module_from_file(file_path, import_path)
        post_endpoint = Endpoint(endpoint_module, 'post')
        patch_endpoint = Endpoint(endpoint_module, 'patch')
        get_endpoint = Endpoint(endpoint_module, 'get')
        cacher = ResolverCache(cache_size=1)
        cacher.put('get::/unit-test/v1/cacher/basic', get_endpoint, False, {})
        get_cache_result = cacher.get('get::/unit-test/v1/cacher/basic')
        self.assertFalse(get_cache_result['endpoint'].has_requirements)
        cacher.put('patch::/unit-test/v1/cacher/basic', patch_endpoint, False, {})
        cacher.get('patch::/unit-test/v1/cacher/basic')
        cacher.put('post::/unit-test/v1/cacher/basic', post_endpoint, False, {})
        cacher.get('post::/unit-test/v1/cacher/basic')
        miss_cache_result = cacher.get('get::/unit-test/v1/cacher/basic')
        self.assertTrue(miss_cache_result.get('endpoint') is None)

    def test_cache_size_none_always_miss(self):
        file_path = f'{self.handler_path}/basic.py'
        import_path = 'tests.mocks.apigateway.cacher.directory_handlers.basic'
        endpoint_module = self.importer.import_module_from_file(file_path, import_path)
        get_endpoint = Endpoint(endpoint_module, 'get')
        cacher = ResolverCache(cache_size=None)
        cacher.put('get::/unit-test/v1/cacher/basic', get_endpoint, False, {})
        get_cache_result = cacher.get('get::/unit-test/v1/cacher/basic')
        self.assertTrue(get_cache_result.get('endpoint') is None)

    def test_cache_static_only(self):
        file_path = f'{self.handler_path}/basic.py'
        import_path = 'tests.mocks.apigateway.cacher.directory_handlers.basic'
        endpoint_module = self.importer.import_module_from_file(file_path, import_path)
        get_endpoint = Endpoint(endpoint_module, 'get')
        cacher = ResolverCache(cache_mode='static-only')
        cacher.put('get::/unit-test/v1/cacher/basic', get_endpoint, False, {})
        get_cache_result = cacher.get('get::/unit-test/v1/cacher/basic')
        self.assertFalse(get_cache_result['endpoint'].has_requirements)
        patch_endpoint = Endpoint(endpoint_module, 'patch')
        cacher.put('patch::/unit-test/v1/cacher/basic', patch_endpoint, True, {'1': 1})
        patch_cache_result = cacher.get('patch::/unit-test/v1/cacher/basic')
        self.assertTrue(patch_cache_result.get('endpoint') is None)

    def test_cache_dynamic_only(self):
        file_path = f'{self.handler_path}/basic.py'
        import_path = 'tests.mocks.apigateway.cacher.directory_handlers.basic'
        endpoint_module = self.importer.import_module_from_file(file_path, import_path)
        get_endpoint = Endpoint(endpoint_module, 'get')
        cacher = ResolverCache(cache_mode='dynamic-only')
        patch_endpoint = Endpoint(endpoint_module, 'patch')
        cacher.put('patch::/unit-test/v1/cacher/basic', patch_endpoint, True, {'1': 1})
        patch_cache_result = cacher.get('patch::/unit-test/v1/cacher/basic')
        self.assertTrue(patch_cache_result['endpoint'].has_requirements)
        cacher.put('get::/unit-test/v1/cacher/basic', get_endpoint, False, {})
        get_cache_result = cacher.get('get::/unit-test/v1/cacher/basic')
        self.assertTrue(get_cache_result.get('endpoint') is None)

    def test_cache_remembers_is_dynamic_route(self):
        file_path = f'{self.handler_path}/basic.py'
        import_path = 'tests.mocks.apigateway.cacher.directory_handlers.basic'
        endpoint_module = self.importer.import_module_from_file(file_path, import_path)
        get_endpoint = Endpoint(endpoint_module, 'get')
        cacher = ResolverCache()
        cacher.put('get::/unit-test/v1/cacher/basic', get_endpoint, True, {'1': 1})
        cached = cacher.get('get::/unit-test/v1/cacher/basic')
        self.assertTrue(cached['is_dynamic_route'])

    def test_cache_remembers_dynamic_parts(self):
        dynamic_parts = {'1': 1}
        file_path = f'{self.handler_path}/basic.py'
        import_path = 'tests.mocks.apigateway.cacher.directory_handlers.basic'
        endpoint_module = self.importer.import_module_from_file(file_path, import_path)
        get_endpoint = Endpoint(endpoint_module, 'get')
        cacher = ResolverCache()
        cacher.put('get::/unit-test/v1/cacher/basic', get_endpoint, True, dynamic_parts)
        cached = cacher.get('get::/unit-test/v1/cacher/basic')
        self.assertDictEqual(cached['dynamic_parts'], dynamic_parts)
