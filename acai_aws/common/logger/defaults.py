import os

from acai_aws.common.logger.common_logger import CommonLogger
from acai_aws.common.logger.redaction import redaction_filter

# Field names redacted by the default PII filter (case-insensitive, any depth).
DEFAULT_PII_KEYS = [
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
]

# Value patterns redacted by the default PII filter.
DEFAULT_PII_PATTERNS = [
    r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}',  # email
    r'\b\d{3}-\d{2}-\d{4}\b',                            # US SSN
    r'\b\d{2}-\d{7}\b',                                  # US EIN / FEIN
    r'\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}',              # US phone
]


def redaction_enabled():
    """Return whether default PII redaction should be registered.

    Controlled by the ``ACAI_LOG_REDACTION`` environment variable; redaction is
    on unless it is set to ``off``, ``false``, ``0``, or ``disabled``.
    """
    setting = os.getenv('ACAI_LOG_REDACTION', 'on').strip().lower()
    return setting not in ('off', 'false', '0', 'disabled')


def register_default_redaction():
    """Register the default PII redaction filter on ``CommonLogger``."""
    CommonLogger.register_callback(
        redaction_filter(keys=DEFAULT_PII_KEYS, patterns=DEFAULT_PII_PATTERNS)
    )
