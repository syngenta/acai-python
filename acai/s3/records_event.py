import csv

import boto3
import jsonpickle

from acai.common.base_records_event import BaseRecordsEvent
from acai.s3.record_event import RecordEvent


class RecordsEvent(BaseRecordsEvent):

    @property
    def records(self):
        self._records = [RecordEvent(record) for record in self._event.get('Records', [])]
        self.__validate_operations()
        self.__get_objects()
        return self.data_classes if self.data_class is not None else self._records

    @property
    def data_classes(self):
        return [self.data_class(record=record) for record in self._records]

    def __validate_operations(self):
        if self._kwargs.get('operations'):
            self._validate_operations(self._kwargs['operations'])

    def __get_objects(self):
        if self._kwargs.get('get_object'):
            client = boto3.client('s3', **self._kwargs.get('s3', {}))
            for record in self._records:
                s3_object_body = client.get_object(Bucket=record.bucket, Key=record.key)['Body']
                if self._kwargs.get('data_type') == 'json':
                    s3_object_body = jsonpickle.decode(s3_object_body.read().decode('utf-8'))
                elif self._kwargs.get('data_type') == 'csv':
                    csv_data = csv.DictReader(s3_object_body.read().decode('utf-8').splitlines(), delimiter=self._kwargs.get('delimiter', ','))
                    s3_object_body = list(csv_data)
                record.body = s3_object_body.copy()
