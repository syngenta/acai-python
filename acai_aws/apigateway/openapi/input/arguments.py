import argparse


class InputArguments:

    def __init__(self):
        args = self.__get_command_line_args()
        self.__base = args.base
        self.__handlers = args.handlers
        self.__output = args.output or args.handlers
        self.__formats = args.format or 'yml'
        self.__delete = args.delete or False

    @property
    def base(self):
        return self.__base

    @property
    def handlers(self):
        return self.__handlers

    @property
    def output(self):
        return self.__output

    @property
    def formats(self):
        return self.__formats.split(',')

    @property
    def delete(self):
        return self.__delete

    def __get_command_line_args(self):
        parser = argparse.ArgumentParser(
            prog='Acai AWS: OpenApi Generator',
            description='Will generate an openapi yml file based on your api project'
        )
        parser.add_argument(
            'action',
            help='the action to take',
            choices=['generate-openapi']
        )
        parser.add_argument(
            '-b',
            '--base',
            help='base path of the api url; (optional) default=/',
            default='/',
            required=False
        )
        parser.add_argument(
            '-l',
            '--handlers',
            help='directory or pattern location of your handlers',
            required=True
        )
        parser.add_argument(
            '-o',
            '--output',
            help='(optional) directory location to save openapi file; defaults handlers directory location',
            required=False
        )
        parser.add_argument(
            '-f',
            '--format',
            help='(optional) comma deliminted format options (yml, json)',
            choices=['yml', 'json', 'yml,json', 'json,yml'],
            required=False
        )
        parser.add_argument(
            '-d',
            '--delete',
            help='(optional) will delete routes and methods not found in code base',
            action='store_true',
            required=False
        )
        return parser.parse_args()
