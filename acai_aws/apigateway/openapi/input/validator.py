import os


class InputValidator:

    def __init__(self):
        self.__yml_exists = False
        self.__json_exists = False
        self.__openapi_dir = None
    
    @property
    def yml_exists(self):
        return self.__yml_exists

    @property
    def json_exists(self):
        return self.__json_exists

    @property
    def openapi_exists(self):
        return self.yml_exists or self.json_exists

    @property
    def existing_openapi_location(self):
        if self.__openapi_dir is None:
            return None
        if self.yml_exists:
            file_extension = 'yml'
        elif self.json_exists:
            file_extension = 'json'
        return f'{self.__openapi_dir}/openapi.{file_extension}'
    
    def validate_arguments(self, input_args):
        self.__check_glob_pattern(input_args.handlers)
        self.__check_directory(input_args.output)
        self.__check_openapi_file_exists(input_args.output)
    
    def __check_glob_pattern(self, handlers):
        if '*.py' not in handlers and not self.__is_directory(handlers):
            raise Exception(f'{handlers} needs to be a glob pattern containing a "*.py" or valid directory location')

    def __check_directory(self, possible_dir):
        if not self.__is_directory(possible_dir):
            raise Exception(f'{possible_dir} is not a valid directory path')
    
    def __is_directory(self, possible_dir):
        return os.path.exists(possible_dir)

    def __check_openapi_file_exists(self, possible_dir):
        if os.path.isfile(f'{possible_dir}/openapi.yml'):
            self.__yml_exists = True
        if os.path.isfile(f'{possible_dir}/openapi.json'):
            self.__json_exists = True
        if self.__yml_exists or self.__json_exists:
            self.__openapi_dir = possible_dir
