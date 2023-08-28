import simplejson as json

def try_decode_json(possible_json):
    try:
        return json.loads(possible_json, use_decimal=True)
    except Exception:
        return possible_json


def try_encode_json(possible_json):
    try:
        return json.dumps(possible_json, use_decimal=True)
    except Exception:
        return possible_json
