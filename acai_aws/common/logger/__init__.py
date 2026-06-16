import logging

from acai_aws.common.logger.common_logger import CommonLogger
from acai_aws.common.logger.redaction import redaction_filter
from acai_aws.common.logger.defaults import (
    DEFAULT_PII_KEYS,
    DEFAULT_PII_PATTERNS,
    redaction_enabled,
    register_default_redaction,
)

__all__ = [
    'log',
    'CommonLogger',
    'redaction_filter',
    'DEFAULT_PII_KEYS',
    'DEFAULT_PII_PATTERNS',
    'redaction_enabled',
    'register_default_redaction',
]

# Register PII redaction by default so every consumer scrubs sensitive fields
# before they are printed (and therefore before they reach CloudWatch). Opt out
# with ACAI_LOG_REDACTION=off, or extend with CommonLogger.register_callback.
if redaction_enabled():
    register_default_redaction()


def log(**kwargs):
    try:
        logger = CommonLogger()
        logger.log(**kwargs)
    except Exception as exception:
        logging.exception(exception)
