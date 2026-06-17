import re


class RedactionFilter:

    DEFAULT_REDACTION = '[REDACTED]'

    def __init__(self, **kwargs):
        self._keys = {str(key).lower() for key in kwargs.get('keys') or []}
        self._patterns = [re.compile(pattern) for pattern in kwargs.get('patterns') or []]
        self._redact_with = kwargs.get('redact_with', self.DEFAULT_REDACTION)

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
