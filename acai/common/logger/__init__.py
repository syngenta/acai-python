import datetime
import logging
import os
import traceback

import jsonpickle

from acai.common.logger.common_logger import CommonLogger


def log(**kwargs):
    try:
        logger = CommonLogger()
        logger.log(**kwargs)
    except Exception as exception:
        logging.exception(exception)
