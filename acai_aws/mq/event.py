from acai_aws.base.event import BaseRecordsEvent
from acai_aws.mq.record import Record


class Event(BaseRecordsEvent):

    def __init__(self, event, context=None, **kwargs):
        super().__init__(event, context, **kwargs)
        self._record_class = Record

    @property
    def raw_messages(self):
        return self._event.get('messages', [])

    @property
    def raw_records(self):
        return self.raw_messages
