import logging

from acai_aws.common.logger.common_logger import CommonLogger


def log(**kwargs):
    try:
        logger = CommonLogger()
        logger.log(**kwargs)
    except Exception as exception:
        logging.exception(exception)
