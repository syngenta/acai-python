import os


class InputValidator:

    def validate_arguments(self, input_args):
        self.__check_glob_pattern(input_args.handlers)
        self.__check_directory(input_args.output)

    def __check_glob_pattern(self, handlers):
        if '*.py' not in handlers:
            raise Exception(f'{handlers} needs to be a glob pattern containing a "*.py" or valid directory location')

    def __check_directory(self, possible_dir):
        if not os.path.exists(possible_dir):
            raise Exception(f'{possible_dir} is not a valid directory path')
