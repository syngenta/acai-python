from acai_aws.base.event import BaseRecordsEvent
from acai_aws.msk.record import Record


class Event(BaseRecordsEvent):

    def __init__(self, event, context=None, **kwargs):
        super().__init__(event, context, **kwargs)
        self._record_class = Record

    @property
    def raw_records(self):
        return self._event.get('records', {})

    def _build_records(self):
        self._records = []
        for topic in self.raw_records:
            for msk_record in self.raw_records[topic]:
                self._records.append(self._record_class(msk_record))

    @property
    def topics(self):
        return list(self.raw_records.keys())
