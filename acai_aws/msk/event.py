from acai_aws.base.event import BaseRecordsEvent
from acai_aws.msk.record import Record


class Event(BaseRecordsEvent):

    def __init__(self, event, context=None, **kwargs):
        super().__init__(event, context, **kwargs)
        self._record_class = Record

    @property
    def raw_records(self):
        return self._event.get('records', {})

    @property
    def records(self):
        self._records = []
        for topic in self.raw_records:
            for msk_record in self.raw_records[topic]:
                self._records.append(self._record_class(msk_record))
        self._validate_operations()
        self._validate_record_body()
        return self.data_classes if self.data_class is not None else self._records

    @property
    def topics(self):
        return list(self.raw_records.keys())
