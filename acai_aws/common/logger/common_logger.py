import datetime
import os
import traceback

import jsonpickle


class CommonLogger:

    _instance = None
    _callbacks = []

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if getattr(self, '_initialized', False):
            return
        self.__json = jsonpickle
        self.__json.set_encoder_options('simplejson', use_decimal=True)
        self.__json.set_preferred_backend('simplejson')
        self.log_levels = {
            'DEBUG': 0,
            'INFO': 1,
            'WARN': 2,
            'WARNING': 2,
            'ERROR': 3,
            'CRITICAL': 4,
            'FATAL': 4,
        }
        self._initialized = True

    @classmethod
    def register_callback(cls, callback):
        if callback in cls._callbacks:
            return
        cls._callbacks.append(callback)

    @classmethod
    def reset_callbacks(cls):
        cls._callbacks = []

    def log(self, **kwargs):
        log_format = (os.getenv('LOG_FORMAT', 'JSON') or 'JSON').strip().upper()
        if log_format not in ('JSON', 'PRETTY', 'INLINE'):
            raise ValueError(f'LOG_FORMAT ENV must be either `JSON`, `PRETTY`, or `INLINE`, recieved: {log_format}')
        level = kwargs.get('level', 'INFO')
        if not self.__should_log(level):
            return
        record = {
            'level': level,
            'time': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'trace': [trace.strip() for trace in self.__get_traceback().split('\n') if trace],
            'log': kwargs.get('log', {}),
        }
        for callback in CommonLogger._callbacks:
            record = callback(record)
        if log_format == 'JSON':
            self.__log_json(record)
        elif log_format == 'PRETTY':
            self.__log_json(record, pretty=True)
        elif log_format == 'INLINE':
            self.__log_inline(record)

    def __get_traceback(self):
        trace = traceback.format_exc()
        if str(trace) != 'NoneType: None\n':
            return trace
        return ''

    def __should_log(self, level):
        log_level = os.getenv('LOG_LEVEL', 'INFO')
        return self.log_levels[level] >= self.log_levels[log_level]

    def __log_json(self, record, pretty=False):
        print(self.__json.encode(record, indent=4 if pretty else None))

    def __log_inline(self, record):
        log_value = record['log']
        if not isinstance(log_value, str):
            log_value = str(log_value)
        inline_message = f"{record['level']}|time={record['time']} log={log_value}"
        trace = ' | '.join(record['trace'])
        if trace:
            inline_message = f"{inline_message} trace={trace}"
        print(inline_message)
