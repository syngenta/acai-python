import os
import glob


class HandlerScanner:

    def __init__(self, handlers):
        self.__handlers = self.clean_path(handlers)

    @property
    def file_separator(self):
        return os.sep

    @property
    def handlers(self):
        return self.__handlers
    
    @property
    def handlers_base(self):
        return self.clean_path(self.__handlers.split('*')[0])
    
    def clean_path(self, dirty_path):
        return dirty_path.strip(self.file_separator)
    
    def get_handler_file_paths(self):
        glob_pattern = self.__get_glob_pattern()
        return glob.glob(glob_pattern, recursive=True)

    def __get_glob_pattern(self):
        if '*' in self.__handlers and '.py' in self.__handlers:
            return self.handlers
        return self.handlers + self.file_separator + '**' + self.file_separator + '*.py'