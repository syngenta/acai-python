import datetime
import os
import traceback

from syngenta_digital_alc.common import json_helper

def log(**kwargs):
    if not os.getenv('RUN_MODE') == 'unittest':
        trace = 'trace not enabled'
        if kwargs.get('trace', False):
            trace = traceback.format_exc()
        print(
            '\n',
            '========== START LOG {} =========='.format(datetime.datetime.now()),
            '\n',
            kwargs.get('level', 'INFO'),
            '\n',
            json_helper.try_encode_json(kwargs.get('log', {})),
            '\n',
            trace,
            '\n',
            '========== END LOG ================'
        )
