import datetime
import os
import traceback

import jsonpickle


class CommonLogger:
    """Structured logger that emits a JSON, pretty JSON, or inline record to stdout.

    Before a record is printed it is passed through any registered callbacks
    (see ``register_callback``). Callbacks are an extension point used for
    redaction, enrichment, or routing; they receive the assembled record dict
    and return the record to emit.
    """

    _callbacks = []

    def __init__(self):
        self.__json = jsonpickle
        env_format = os.getenv('LOG_FORMAT', 'JSON') or 'JSON'
        self.__format = env_format.strip().upper()
        self.__log_level = os.getenv('LOG_LEVEL', 'INFO')
        self.__json.set_encoder_options('simplejson', use_decimal=True)
        self.__json.set_preferred_backend('simplejson')
        self.log_levels = {
            'DEBUG': 0,
            'INFO': 1,
            'WARN': 2,
            'WARNING': 2,
            'ERROR': 3,
            'CRITICAL': 4,
            'FATAL': 4
        }
        if self.__format not in ['JSON', 'PRETTY', 'INLINE']:
            raise ValueError(f'LOG_FORMAT ENV must be either `JSON`, `PRETTY`, or `INLINE`, recieved: {self.__format}')

    @classmethod
    def register_callback(cls, callback):
        """Register a callable run on every log record before it is printed.

        The callback signature is ``callback(record: dict) -> dict`` where
        ``record`` holds ``level``, ``time``, ``trace``, and ``log``. The
        returned record is what gets emitted, so a callback may mutate or
        replace any part of it. Callbacks run in registration order.
        """
        cls._callbacks.append(callback)

    @classmethod
    def reset_callbacks(cls):
        """Remove all registered callbacks."""
        cls._callbacks = []

    def log(self, **kwargs):
        """Build a log record, run it through registered callbacks, and emit it."""
        level = kwargs.get('level', 'INFO')
        if not self.__should_log(level):
            return
        record = {
            'level': level,
            'time': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'trace': [trace.strip() for trace in self.__get_traceback().split('\n') if trace],
            'log': kwargs.get('log', {})
        }
        for callback in CommonLogger._callbacks:
            record = callback(record)
        if self.__format == 'JSON':
            self.__log_json(record)
        elif self.__format == 'PRETTY':
            self.__log_json(record, pretty=True)
        elif self.__format == 'INLINE':
            self.__log_inline(record)

    def __get_traceback(self):
        trace = traceback.format_exc()
        if str(trace) != 'NoneType: None\n':
            return trace
        return ''

    def __should_log(self, level):
        current_log_level = self.log_levels[level]
        log_level_setting = self.log_levels[self.__log_level]
        return current_log_level >= log_level_setting

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
