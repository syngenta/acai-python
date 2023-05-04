from acai.common.records.base import BaseRecords
from acai.common.records.common_record import CommonRecord


class CommonRecords(BaseRecords):

    def __init__(self, event, context=None, **kwargs):
        super().__init__(event, context, **kwargs)
        self._record_class = CommonRecord
        self._records = [event]

    @property
    def raw_records(self):
        return self._records

    @property
    def data_classes(self):
        return [self.data_class(record=record) for record in self._records]

    @property
    def records(self):
        return self._records
