import datetime
import os
import traceback

import jsonpickle


class CommonLogger:

    def __init__(self):
        self.default_level = 3
        self.log_levels = {
            'INFO': 1,
            'WARN': 2,
            'ERROR': 3
        }

    def log(self,**kwargs):
        if not os.getenv('RUN_MODE') == 'unittest' and os.getenv('STAGE') == 'local' and self.__should_log():
            self.__log_local(**kwargs)
        elif not os.getenv('RUN_MODE') == 'unittest' and self.__should_log():
            self.__log(**kwargs)

    def __log_local(self, **kwargs):
        print(jsonpickle.encode({
            'level': kwargs.get('level', 'INFO'),
            'time': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'stack': traceback.format_exc().splitlines(),
            'log': kwargs.get('log', {})
        }, indent=4))

    def __log(self, **kwargs):
        print(jsonpickle.encode({
            'level': kwargs.get('level', 'INFO'),
            'time': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'stack': traceback.format_exc().splitlines(),
            'log': kwargs.get('log', {})
        }))

    def __should_log(self, **kwargs):
        log_setting = self.__get_current_log_setting()
        log_level = self.__get_log_level(**kwargs)
        return log_level <= log_setting

    def __get_current_log_setting(self):
        log_setting = os.getenv('LOG_LEVEL', 'INFO')
        if not log_setting.isnumeric():
            return self.log_levels[log_setting] if log_setting in self.log_levels else 'ERROR'
        return int(log_setting)

    def __get_log_level(self, **kwargs):
        log_level = kwargs.get('level', 'INFO')
        if log_level.isnumeric():
            return int(log_level)
        if log_level in self.log_levels:
            return self.log_levels[log_level]
        return self.default_level


def log(**kwargs):
    try:
        logger = CommonLogger()
        logger.log(**kwargs)
    except Exception as error:
        print(error)
