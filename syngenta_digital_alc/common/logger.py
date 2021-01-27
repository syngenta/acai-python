import datetime
import os
import traceback

from syngenta_digital_alc.common import json_helper

def log(**kwargs):
    if not os.getenv('RUN_MODE') == 'unittest':
        print(json_helper.try_encode_json({
            'level': kwargs.get('level', 'INFO'),
            'time': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'stack': traceback.format_exc().splitlines(),
            'log': kwargs.get('log', {})
        }))
