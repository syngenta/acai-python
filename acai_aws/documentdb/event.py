from acai_aws.base.event import BaseRecordsEvent
from acai_aws.documentdb.record import Record


class Event(BaseRecordsEvent):

    def __init__(self, event, context=None, **kwargs):
        super().__init__(event, context, **kwargs)
        self._record_class = Record

    @property
    def raw_events(self):
        return self._event.get('events', [])

    @property
    def raw_records(self):
        return self.raw_events

    @property
    def events(self):
        return self.records
