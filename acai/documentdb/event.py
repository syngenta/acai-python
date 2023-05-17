from acai.base.event import BaseRecordsEvent
from acai.documentdb.record import Record


class Event(BaseRecordsEvent):

    def __init__(self, event, context=None, **kwargs):
        super().__init__(event, context, **kwargs)
        self._record_class = Record

    @property
    def raw_events(self):
        return self._event.get('events', [])

    @property
    def events(self):
        self._records = [self._record_class(record) for record in self.raw_events]
        self._validate_operations()
        self._validate_record_body()
        return self.data_classes if self.data_class is not None else self._records

    @property
    def records(self):
        return self.events
