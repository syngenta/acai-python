import json
import unittest

from acai.apigateway.importer import Importer


def serialize_sets(obj):
    if isinstance(obj, set):
        return list(obj)
    return obj


class ImporterTest(unittest.TestCase):
    handler_path = 'tests/mocks/apigateway/directory-handlers'
    handler_pattern = 'tests/mocks/apigateway/pattern-handlers/**/*_controller.py'

    def test_clean_path(self):
        dirty_path = '/tests/mocks/apigateway/directory-handlers/'
        clean_path = Importer.clean_path(dirty_path)
        self.assertEqual(clean_path, self.handler_path)

    def test_get_absolute_handler_path(self):
        importer = Importer(handlers=self.handler_path, mode='directory')
        abs_handler_path = importer.get_absolute_handler_path()
        self.assertTrue('tests/mocks/apigateway/directory-handlers' in abs_handler_path)

    def test_get_glob_pattern_directory_mode(self):
        importer = Importer(handlers=self.handler_path, mode='directory')
        abs_handler_path = importer.get_glob_pattern()
        self.assertTrue('tests/mocks/apigateway/directory-handlers/**/*.py' in abs_handler_path)

    def test_get_glob_pattern_pattern_mode(self):
        importer = Importer(handlers=self.handler_pattern, mode='pattern')
        abs_handler_path = importer.get_glob_pattern()
        self.assertTrue('tests/mocks/apigateway/pattern-handlers/**/*_controller.py' in abs_handler_path)

    def test_list_files_in_handler_directory(self):
        importer = Importer(handlers=self.handler_path, mode='directory')
        files = importer.list_files_in_handler_path()
        print('files', files)
        self.assertTrue(len(files) >= 1)

    def test_list_files_by_handler_pattern(self):
        importer = Importer(handlers=self.handler_pattern, mode='pattern')
        files = importer.list_files_in_handler_path()
        print('files', files)
        self.assertTrue(len(files) >= 1)

    # def test_get_file_tree(self):
    #     importer = Importer(handlers=self.handler_path, mode='directory')
    #     tree = importer.get_file_tree()
    #     print(json.dumps(tree, indent=4, default=serialize_sets))
