import csv

import boto3
import jsonpickle

from acai.common.records import CommonRecords
from acai.dynamodb.record import Record


class Records(CommonRecords):

    @property
    def records(self):
        self._records = [Record(record) for record in self._event.get('Records', [])]
        self._validate_operations()
        self._validate_record_body()
        return self.data_classes if self.data_class is not None else self._records
