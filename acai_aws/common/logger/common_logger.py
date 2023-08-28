import datetime
import os
import traceback

import jsonpickle


class CommonLogger:

    def __init__(self):
        self.__json = jsonpickle
        self.__run_mode = os.getenv('RUN_MODE')
        self.__log_level = os.getenv('LOG_LEVEL', 'INFO')
        self.__stage_variable = os.getenv('LOG_LOCAL_STAGE_VARIABLE', 'STAGE')
        self.__stage_name = os.getenv('LOG_LOCAL_STAGE_NAME', 'local')
        self.__log_stage = os.getenv(self.__stage_variable)
        self.__json.set_encoder_options('simplejson', use_decimal=True)
        self.__json.set_preferred_backend('simplejson')
        self.log_levels = {
            'INFO': 1,
            'WARN': 2,
            'ERROR': 3
        }

    def log(self, **kwargs):
        default_log = {
            'level': kwargs.get('level', 'INFO'),
            'log': kwargs.get('log', {})
        }
        if not self.__run_mode == 'unittest' and self.__log_stage == self.__stage_name and self.__should_log(**default_log):
            self.__log_local(**default_log)
        elif not self.__run_mode == 'unittest' and self.__should_log(**default_log):
            self.__log(**default_log)

    def __log_local(self, **kwargs):
        stack = self.__clean_up_stack_trace(kwargs['log'])
        print(self.__json.encode({
            'level': kwargs['level'],
            'time': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'stack': stack,
            'log': kwargs['log']
        }, indent=4))

    def __log(self, **kwargs):
        stack = self.__clean_up_stack_trace(kwargs['log'])
        print(self.__json.encode({
            'level': kwargs['level'],
            'time': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'stack': stack,
            'log': kwargs['log']
        }))

    def __clean_up_stack_trace(self, log_object):
        if isinstance(log_object, Exception):
            return traceback.format_exc().splitlines()
        skip = False
        new_line_split = [stack.split('\n') for stack in traceback.format_stack()]
        stack_trace = []
        for new_split in new_line_split:
            for new_line in new_split:
                if 'acai/common/logger' in new_line:
                    skip = True
                if new_line and not skip:
                    stack_trace.append(new_line)
        return stack_trace

    def __should_log(self, **kwargs):
        current_log_level = self.log_levels[kwargs['level']]
        log_level_setting = self.log_levels[self.__log_level]
        return current_log_level >= log_level_setting
