import os
import unittest

from acai.apigateway.importer import Importer


class ImporterTest(unittest.TestCase):
    maxDiff = None
    handler_path = 'tests/mocks/importer/directory-handlers'
    handler_pattern = 'tests/mocks/importer/pattern-handlers/**/*_controller.py'
    expected_directory_file_tree = {
        "__dynamic_file_count": set(),
        "__init__.py": "*",
        "basic.py": "*",
        "nested-1": {
            "__dynamic_file_count": set(),
            "nested-2": {
                "__dynamic_file_count": set(),
                "basic.py": "*"
            }
        }
    }
    expected_pattern_file_tree = {
        "__dynamic_file_count": set(),
        "basic_controller.py": "*",
        "nested-1": {
            "__dynamic_file_count": set(),
            "nested-2": {
                "__dynamic_file_count": set(),
                "basic_controller.py": "*"
            }
        }
    }

    def test_clean_path(self):
        self.assertEqual(Importer.clean_path('/dirty/path/'), 'dirty/path')

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
