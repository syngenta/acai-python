import glob
import os


class Importer:
    PATTERN_MODE = 'pattern'
    DIRECTORY_MODE = 'directory'

    def __init__(self, **kwargs):
        self.__mode = kwargs['mode']
        self.__handlers = Importer.clean_path(kwargs['handlers'])
        self.__handlers_root = None
        self.__handlers_tree = {}
        self.__project_root = None

    @staticmethod
    def clean_path(dirty_path):
        return dirty_path.strip(os.sep)

    @property
    def project_root(self):
        if not self.__project_root:
            path = os.path.normpath(self.handlers)
            handler_root = path.split(os.sep)[0]
            self.__project_root = Importer.clean_path(os.getcwd().split(handler_root)[0])
        return self.__project_root

    @property
    def handlers(self):
        return self.__handlers

    @property
    def handlers_root(self):
        if not self.__handlers_root:
            sep_split = self.__handlers.split(os.sep)
            cleaned_split = [directory for directory in sep_split if '*' not in directory]
            self.__handlers_root = Importer.clean_path(f'{os.sep}'.join(cleaned_split))
        return self.__handlers_root

    @property
    def handlers_path_abs(self):
        return os.sep + self.project_root + os.sep + self.handlers_root

    @property
    def handlers_file_tree(self):
        if not self.__handlers_tree:
            glob_pattern = self.__get_glob_pattern()
            file_list = glob.glob(glob_pattern, recursive=True)
            file_paths = [item.replace(self.handlers_path_abs + os.sep, '') for item in file_list]
            for file_path in file_paths:
                sections = file_path.split(os.sep)
                self.__recurse_section(self.__handlers_tree, sections, 0)
        return self.__handlers_tree

    def __get_glob_pattern(self):
        if self.__mode == self.PATTERN_MODE:
            return os.sep + self.project_root + os.sep + self.handlers
        return self.handlers_path_abs + os.sep + '**' + os.sep + '*.py'

    def __recurse_section(self, file_leaf, sections, index):
        if index >= len(sections):
            return
        section = sections[index]
        if not section:
            self.__recurse_section(file_leaf, sections, index + 1)
        if section not in file_leaf:
            file_leaf[section] = {} if index + 1 < len(sections) else '*'
        if isinstance(file_leaf, dict) and '__dynamic_files' not in file_leaf:
            file_leaf['__dynamic_files'] = set()
        if section.startswith('_') and section != '__init__.py':
            file_leaf['__dynamic_files'].add(section)
        self.__recurse_section(file_leaf[section], sections, index + 1)
