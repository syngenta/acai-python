import datetime
import os
import traceback

import jsonpickle


class CommonLogger:

    def __init__(self):
        self.__json = jsonpickle
        env_format = os.getenv('LOG_FORMAT', 'JSON') or 'JSON'
        self.__format = env_format.strip().upper()
        self.__log_level = os.getenv('LOG_LEVEL', 'INFO')
        self.__json.set_encoder_options('simplejson', use_decimal=True)
        self.__json.set_preferred_backend('simplejson')
        self.log_levels = {
            'INFO': 1,
            'WARN': 2,
            'ERROR': 3
        }
        if self.__format not in ['JSON', 'INLINE']:
            raise ValueError(f'LOG_FORMAT ENV must be either `JSON` or `INLINE`, recieved: {self.__format}')

    def log(self, **kwargs):
        default_log = {'level': kwargs.get('level', 'INFO'), 'log': kwargs.get('log', {})}
        if self.__should_log(default_log['level']) and self.__format == 'JSON':
            self.__log_json(**kwargs)
        elif self.__should_log(default_log['level']) and self.__format == 'INLINE':
            self.__log_inline(**kwargs)

    def __get_traceback(self):
        trace = traceback.format_exc()
        if str(trace) != 'NoneType: None\n':
            return trace
        return ''

    def __should_log(self, level):
        current_log_level = self.log_levels[level]
        log_level_setting = self.log_levels[self.__log_level]
        return current_log_level >= log_level_setting

    def __log_json(self, **kwargs):
        print(self.__json.encode({
            'level': kwargs['level'],
            'time': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'trace': [trace.strip() for trace in self.__get_traceback().split('\n') if trace],
            'log': kwargs['log']
        }, indent=4))

    def __log_inline(self, **kwargs):
        timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        trace = self.__get_traceback().strip().replace('\n', ' | ')
        log_value = kwargs['log']
        if not isinstance(log_value, str):
            log_value = str(log_value)
        inline_message = f"{kwargs['level']}|time={timestamp} log={log_value}"
        if trace:
            inline_message = f"{inline_message} trace={trace}"
        print(inline_message)
