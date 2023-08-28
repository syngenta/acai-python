import base64

from acai_aws.common.json_helper import JsonHelper
from acai_aws.base.record import BaseRecord


class Record(BaseRecord):

    @property
    def record_id(self):
        return self._record.get('recordId')

    @property
    def epoc_time_stamp(self):
        return self._record.get('approximateArrivalTimestamp')

    @property
    def shard_id(self):
        return self._record.get('kinesisRecordMetadata', {}).get('shardId')

    @property
    def partition_key(self):
        return self._record.get('kinesisRecordMetadata', {}).get('partitionKey')

    @property
    def time_stamp(self):
        return self._record.get('kinesisRecordMetadata', {}).get('approximateArrivalTimestamp')

    @property
    def sequence_number(self):
        return self._record.get('kinesisRecordMetadata', {}).get('sequenceNumber')

    @property
    def subsequence_number(self):
        return self._record.get('kinesisRecordMetadata', {}).get('subsequenceNumber')

    @property
    def data(self):
        b64_decoded = base64.b64decode(self._record.get('data')).decode('utf-8')
        return JsonHelper.decode(b64_decoded)

    @property
    def body(self):
        return self.data

    @property
    def operation(self):
        return self.UNKNOWN

    def __str__(self):
        return str({
            'record_id': self.record_id,
            'epoc_time_stamp': self.epoc_time_stamp,
            'shard_id': self.shard_id,
            'partition_key': self.partition_key,
            'time_stamp': self.time_stamp,
            'sequence_number': self.sequence_number,
            'subsequence_number': self.subsequence_number,
            'body': self.body,
            'operation': self.operation
        })
