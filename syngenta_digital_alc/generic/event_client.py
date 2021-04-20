from syngenta_digital_alc.common import json_helper

class EventClient:

    def __init__(self, event, context):
        self._event = event
        self.context = context

    @property
    def body(self):
        return json_helper.try_decode_json(self._event)

    @property
    def raw_body(self):
        return self._event
