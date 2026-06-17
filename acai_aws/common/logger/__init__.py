import logging

from acai_aws.common.logger.common_logger import CommonLogger
from acai_aws.common.logger.redaction import RedactionFilter

__all__ = ['log', 'CommonLogger', 'RedactionFilter']


def log(**kwargs):
    try:
        logger = CommonLogger()
        logger.log(**kwargs)
    except Exception as exception:
        logging.exception(exception)
