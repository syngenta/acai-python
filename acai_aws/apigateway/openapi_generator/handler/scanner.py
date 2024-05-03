import os
import glob


class HandlerScanner:

    def __init__(self, handlers):
        self.__handlers =  self.clean_path(handlers)
        self.__SUPPORTED_METHODS = ['any', 'delete', 'get', 'head', 'options', 'patch', 'post', 'put']
        self.__modules = []

    @property
    def file_separator(self):
        return os.sep

    @property
    def handlers(self):
        return self.__handlers
    
    def clean_path(self, dirty_path):
        return dirty_path.strip(self.file_separator)
    
    def get_handler_modules(self):
        glob_pattern = self.__get_glob_pattern()
        file_list = glob.glob(glob_pattern, recursive=True)
        return file_list

    def __get_glob_pattern(self):
        if '*' in self.__handlers and '.py' in self.__handlers:
            return self.handlers
        return self.handlers + self.file_separator + '**' + self.file_separator + '*.py'
        