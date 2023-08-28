from acai_aws.common.json_helper import JsonHelper


class Event:

    def __init__(self, event, context=None):
        self._event = event
        self._context = context

    @property
    def body(self):
        return JsonHelper.decode(self._event)
