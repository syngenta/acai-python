import importlib.util
import glob
import os

from acai_aws.apigateway.exception import ApiException


class ResolverImporter:

    def __init__(self, **kwargs):
        self.__handlers = self.clean_path(kwargs['handlers'])
        self.__handlers_tree = {}

    @staticmethod
    def import_module_from_file(file_path, import_path):
        spec = importlib.util.spec_from_file_location(import_path, file_path)
        handler_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(handler_module)
        return handler_module

    @property
    def file_separator(self):
        return os.sep

    @property
    def handlers(self):
        return self.__handlers

    def clean_path(self, dirty_path):
        return dirty_path.strip(self.file_separator)

    def get_handlers_file_tree(self):
        if not self.__handlers_tree:
            glob_pattern = self.__get_glob_pattern()
            file_list = glob.glob(glob_pattern, recursive=True)
            file_paths = [item.replace(self.__get_handlers_root(), '') for item in file_list]
            for file_path in file_paths:
                sections = file_path.split(self.file_separator)
                sections = [section for section in sections if section]
                self.__recurse_section(self.__handlers_tree, sections, 0)
        return self.__handlers_tree

    def __get_glob_pattern(self):
        if '*' in self.__handlers and '.py' in self.__handlers:
            return self.handlers
        return self.handlers + self.file_separator + '**' + self.file_separator + '*.py'
    
    def __get_handlers_root(self):
        if '*' in self.__handlers and '.py' in self.__handlers:
            sep_split = self.handlers.split(self.file_separator)
            cleaned_split = [directory for directory in sep_split if self.__is_directory(directory)]
            return self.clean_path(f'{self.file_separator}'.join(cleaned_split))
        return self.handlers
    
    def __is_directory(self, directory):
        if '*' not in directory and '.py' not in directory:
            return True
        return False

    def __recurse_section(self, file_leaf, sections, index):
        if not index < len(sections):
            return
        section = sections[index]
        if not section: # pragma: no cover
            self.__recurse_section(file_leaf, sections, index + 1)
        if section not in file_leaf:
            file_leaf[section] = {} if index + 1 < len(sections) else '*'
        if isinstance(file_leaf, dict) and '__dynamic_files' not in file_leaf:
            file_leaf['__dynamic_files'] = set()
        if section.startswith('_') and not section.startswith('__'):
            file_leaf['__dynamic_files'].add(section)
        self.__check_multiple_dynamic_files(file_leaf, sections)
        self.__check_file_and_directory_share_name(file_leaf, section, sections)
        self.__recurse_section(file_leaf[section], sections, index + 1)

    def __check_multiple_dynamic_files(self, file_leaf, sections):
        if len(file_leaf['__dynamic_files']) > 1:
            files = ', '.join(list(file_leaf['__dynamic_files']))
            sections.pop()
            location = f'{self.file_separator}'.join(sections)
            raise ApiException(message=f'Cannot have two dynamic files in the same directory. Files: {files}, Location: {location}')

    def __check_file_and_directory_share_name(self, file_leaf, section, sections):
        opposite_type = section.replace('.py', '') if '.py' in section else f'{section}.py'
        if opposite_type in file_leaf:
            location = f'{self.file_separator}'.join(sections)
            raise ApiException(message=f'Cannot have file and directory share same name. Files: {section}, Location: {location}')
