import os
import re


class RedactionFilter:

    DEFAULT_REDACTION = '[REDACTED]'
    REDACTION_ENV = 'ACAI_LOG_REDACTION'
    DISABLED_VALUES = ('off', 'false', '0', 'disabled')

    DEFAULT_KEYS = (
        'first_name',
        'last_name',
        'worker_first_name',
        'worker_last_name',
        'email',
        'worker_email',
        'phone',
        'worker_phone',
        'ssn',
        'social_security_number',
        'fein',
        'ein',
    )

    DEFAULT_PATTERNS = (
        r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}',
        r'\b\d{3}-\d{2}-\d{4}\b',
        r'\b\d{2}-\d{7}\b',
        r'\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}',
    )

    def __init__(self, **kwargs):
        self._keys = {str(key).lower() for key in kwargs.get('keys') or []}
        self._patterns = [re.compile(pattern) for pattern in kwargs.get('patterns') or []]
        self._redact_with = kwargs.get('redact_with', self.DEFAULT_REDACTION)

    @classmethod
    def register_default(cls, logger_class):
        if os.environ.get(cls.REDACTION_ENV, 'on').strip().lower() in cls.DISABLED_VALUES:
            return
        logger_class.register_callback(cls(keys=cls.DEFAULT_KEYS, patterns=cls.DEFAULT_PATTERNS))

    def __call__(self, record):
        if isinstance(record, dict) and 'log' in record:
            record['log'] = self._scrub(record['log'])
        return record

    def _scrub(self, value):
        if isinstance(value, dict):
            return {key: self._scrub_field(key, item) for key, item in value.items()}
        if isinstance(value, (list, tuple)):
            return [self._scrub(item) for item in value]
        if isinstance(value, str):
            return self._scrub_text(value)
        return value

    def _scrub_field(self, key, value):
        if str(key).lower() in self._keys:
            return self._redact_with
        return self._scrub(value)

    def _scrub_text(self, value):
        for pattern in self._patterns:
            value = pattern.sub(self._redact_with, value)
        return value
