import csv

import boto3
import jsonpickle

from acai.common.records import CommonRecords
from acai.s3.record import Record


class Records(CommonRecords):

    @property
    def records(self):
        self._records = [Record(record) for record in self._event.get('Records', [])]
        self._validate_operations()
        self.__get_objects()
        self._validate_record_body()
        return self.data_classes if not self.data_class else self._records

    def __get_objects(self):
        if not self._kwargs.get('get_object'):
            return
        client = boto3.client('s3', **self._kwargs.get('s3', {}))
        for record in self._records:
            s3_object_body = client.get_object(Bucket=record.bucket, Key=record.key)['Body']
            if self._kwargs.get('data_type') == 'json':
                s3_object_body = jsonpickle.decode(s3_object_body.read().decode('utf-8'))
            elif self._kwargs.get('data_type') == 'csv':
                csv_data = csv.DictReader(s3_object_body.read().decode('utf-8').splitlines(), delimiter=self._kwargs.get('delimiter', ','))
                s3_object_body = list(csv_data)
            record.body = s3_object_body.copy()
