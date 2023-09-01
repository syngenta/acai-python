import datetime
import os
import traceback

import jsonpickle


class CommonLogger:

    def __init__(self):
        self.__json = jsonpickle
        self.__log_level = os.getenv('LOG_LEVEL', 'INFO')
        self.__json.set_encoder_options('simplejson', use_decimal=True)
        self.__json.set_preferred_backend('simplejson')
        self.log_levels = {
            'INFO': 1,
            'WARN': 2,
            'ERROR': 3
        }

    def log(self, **kwargs):
        default_log = {'level': kwargs.get('level', 'INFO'), 'log': kwargs.get('log', {})}
        if self.__should_log(default_log['level']):
            print(self.__json.encode({
                'level': kwargs['level'],
                'time': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                'stack': [trace.strip() for trace in traceback.format_exc().split('\n') if trace],
                'log': kwargs['log']
            }, indent=4))

    def __should_log(self, level):
        current_log_level = self.log_levels[level]
        log_level_setting = self.log_levels[self.__log_level]
        return current_log_level >= log_level_setting
