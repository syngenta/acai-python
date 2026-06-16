import re

DEFAULT_REDACTION = '[REDACTED]'


def redaction_filter(keys=None, patterns=None, redact_with=DEFAULT_REDACTION):
    """Build a logger callback that redacts sensitive data from the log payload.

    ``keys`` are field names redacted wherever they appear in the ``log``
    payload (case-insensitive, at any nesting depth). ``patterns`` are regular
    expression strings; every match found in a string value is replaced.
    ``redact_with`` is the replacement text (default ``[REDACTED]``); pass
    ``redact_with=''`` or any custom string to override it.

    Returns a callback compatible with ``CommonLogger.register_callback``; the
    custom filter therefore rides on the generic callback hook rather than
    special-casing the logger.
    """
    lowered_keys = {str(key).lower() for key in (keys or [])}
    compiled_patterns = [re.compile(pattern) for pattern in (patterns or [])]

    def scrub(value):
        if isinstance(value, dict):
            return {
                key: redact_with if str(key).lower() in lowered_keys else scrub(item)
                for key, item in value.items()
            }
        if isinstance(value, (list, tuple)):
            return [scrub(item) for item in value]
        if isinstance(value, str):
            redacted = value
            for pattern in compiled_patterns:
                redacted = pattern.sub(redact_with, redacted)
            return redacted
        return value

    def callback(record):
        if isinstance(record, dict) and 'log' in record:
            record['log'] = scrub(record['log'])
        return record

    return callback
