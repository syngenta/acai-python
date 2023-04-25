from acai.common.base_records_event import BaseRecordsEvent
from acai.s3.record_event import RecordEvent


class RecordsEvent(BaseRecordsEvent):

    @property
    def records(self):
        self._records = [RecordEvent(record) for record in self._event.get('Records', [])]
        if self._kwargs.get('operations'):
            self._validate_operations(self._kwargs['operations'])
        if self.data_class is not None:
            return self.data_classes
        return self._records

    @property
    def data_classes(self):
        return [self.data_class(record=record) for record in self._records]
