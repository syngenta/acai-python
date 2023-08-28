from acai_aws.base.event import BaseRecordsEvent
from acai_aws.common.records.record import Record


class Event(BaseRecordsEvent):

    def __init__(self, event, context=None, **kwargs):
        super().__init__(event, context, **kwargs)
        self._record_class = Record
        self._records = event if isinstance(event, list) else [event]

    @property
    def raw_records(self):
        return self._records

    @property
    def records(self):
        self._records = [self._record_class(record) for record in self.raw_records]
        return self.data_classes if self.data_class is not None else self._records
