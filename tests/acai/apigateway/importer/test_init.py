import os
import unittest

from acai.apigateway.importer import Importer
from acai.apigateway.importer.exception import ImporterException


class ImporterTest(unittest.TestCase):
    maxDiff = None
    handler_path = 'tests/mocks/importer/directory-handlers'
    handler_pattern = 'tests/mocks/importer/pattern-handlers/**/*_controller.py'
    handler_bad_multi_dynamic = 'tests/mocks/importer/bad-handlers/multi-dynamic'
    handler_bad_same_name = 'tests/mocks/importer/bad-handlers/same-name'
    expected_directory_file_tree = {
        '__dynamic_files': {'_dynamic'},
        'basic.py': '*',
        '_dynamic': {
            '__dynamic_files': set(),
            '__init__.py': '*'
        },
        'nested_1': {
            '__dynamic_files': set(),
            'nested_2': {
                '__dynamic_files': {'_id.py'},
                'basic.py': '*',
                '_id.py': '*'
            }
        }
    }
    expected_pattern_file_tree = {
        '__dynamic_files': {'_dynamic'},
        'basic_controller.py': '*',
        '_dynamic': {
            '__dynamic_files': set(),
            'dynamic_controller.py': '*'
        },
        'nested_1': {
            '__dynamic_files': set(),
            'nested_2': {
                '__dynamic_files': {'_id_controller.py'},
                'basic_controller.py': '*',
                '_id_controller.py': '*'
            }
        }
    }

    def test_clean_path(self):
        importer = Importer(handlers=self.handler_path, mode='directory')
        self.assertEqual(importer.clean_path('/dirty/path/'), 'dirty/path')

    def test_project_root(self):
        importer = Importer(handlers=self.handler_path, mode='directory')
        self.assertTrue(os.sep in importer.project_root)

    def test_clean_handlers(self):
        importer = Importer(handlers=self.handler_path, mode='directory')
        self.assertEqual(importer.handlers, self.handler_path)

    def test_dirty_handlers(self):
        dirty_path = '/tests/mocks/importer/directory-handlers/'
        importer = Importer(handlers=dirty_path, mode='directory')
        self.assertEqual(importer.handlers, self.handler_path)

    def test_handlers_root_directory_handlers(self):
        importer = Importer(handlers=self.handler_path, mode='directory')
        self.assertEqual(importer.handlers_root, 'tests/mocks/importer/directory-handlers')

    def test_handlers_root_pattern_handlers(self):
        importer = Importer(handlers=self.handler_pattern, mode='pattern')
        self.assertEqual(importer.handlers_root, 'tests/mocks/importer/pattern-handlers')

    def test_handlers_path_abs_directory_mode(self):
        importer = Importer(handlers=self.handler_path, mode='directory')
        self.assertTrue('/tests/mocks/importer/directory-handlers' in importer.handlers_path_abs)

    def test_handlers_path_abs_pattern_mode(self):
        importer = Importer(handlers=self.handler_pattern, mode='pattern')
        self.assertTrue('/tests/mocks/importer/pattern-handlers' in importer.handlers_path_abs)

    def test_handlers_file_tree_directory_mode(self):
        importer = Importer(handlers=self.handler_path, mode='directory')
        self.assertDictEqual(self.expected_directory_file_tree, importer.handlers_file_tree)

    def test_handlers_file_tree_pattern_mode(self):
        importer = Importer(handlers=self.handler_pattern, mode='pattern')
        self.assertDictEqual(self.expected_pattern_file_tree, importer.handlers_file_tree)

    def test_handlers_file_throw_exception_on_two_dynamic_files(self):
        importer = Importer(handlers=self.handler_bad_multi_dynamic, mode='directory')
        try:
            print(importer.handlers_file_tree)
        except ImporterException as importer_error:
            self.assertTrue(isinstance(importer_error, ImporterException))
            self.assertTrue('Can not have two dynamic files in the same directory.' in importer_error.message)
            
