import csv

import boto3

from acai_aws.common.json_helper import JsonHelper
from acai_aws.base.event import BaseRecordsEvent
from acai_aws.s3.record import Record


class Event(BaseRecordsEvent):

    def __init__(self, event, context=None, **kwargs):
        super().__init__(event, context, **kwargs)
        self._record_class = Record

    def _post_operation_hook(self):
        self.__get_objects()

    def __get_objects(self):
        if not self._kwargs.get('get_object'):
            return
        client = boto3.client('s3', **self._kwargs.get('s3', {}))
        for record in self._records:
            s3_object_body = client.get_object(Bucket=record.bucket, Key=record.key)['Body']
            if self._kwargs.get('data_type') == 'json':
                s3_object_body = JsonHelper.decode(s3_object_body.read().decode('utf-8'), True)
            elif self._kwargs.get('data_type') == 'csv':
                csv_data = csv.DictReader(s3_object_body.read().decode('utf-8').splitlines(), delimiter=self._kwargs.get('delimiter', ','))
                s3_object_body = list(csv_data)
            record.body = s3_object_body.copy()
