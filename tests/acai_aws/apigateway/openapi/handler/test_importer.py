import unittest

from acai_aws.apigateway.openapi.handler.importer import HandlerImporter


class HandlerImporterTest(unittest.TestCase):

    def test_get_modules_from_file_paths(self):
        importer = HandlerImporter()
        file_paths = ['tests/mocks/apigateway/openapi/basic.py']
        handlers_base = 'tests/mocks/apigateway/openapi'
        base_path = 'acai_aws/example'
        modules = importer.get_modules_from_file_paths(file_paths, handlers_base, base_path)
        assert len(modules) == 2