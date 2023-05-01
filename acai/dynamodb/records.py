from acai.common.records import CommonRecords
from acai.common.records.exception import NoDataClass
from acai.dynamodb.record import Record


class Records(CommonRecords):

    @property
    def records(self):
        self._records = [Record(record) for record in self._event.get('Records', [])]
        self._validate_operations()
        self._validate_record_body()
        return self.data_classes if not isinstance(self.data_class, NoDataClass) else self._records
