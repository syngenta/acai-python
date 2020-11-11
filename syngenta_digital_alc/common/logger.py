import datetime
import os
import traceback

from syngenta_digital_alc.common import json_helper

def log(**kwargs):
    if not os.getenv('RUN_MODE') == 'unittest':
        print(json_helper.try_encode_json({
            'level': kwargs.get('level', 'INFO'),
            'time': datetime.datetime.now(),
            'stack': traceback.format_exc(),
            'log': kwargs.get('log', {})
        }))
