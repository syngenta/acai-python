from acai.common.base_records_event import BaseRecordsEvent
from acai.s3.record_event import RecordEvent


class RecordsEvent(BaseRecordsEvent):

    @property
    def records(self):
        if self.data_class is not None:
            return self.data_classes
        return [RecordEvent(record) for record in self._event.get('Records', [])]

    @property
    def data_classes(self):
        return [self.data_class(record=RecordEvent(record)) for record in self._event.get('Records', [])]


