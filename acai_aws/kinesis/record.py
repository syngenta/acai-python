import base64

from acai_aws.common.json_helper import JsonHelper
from acai_aws.base.record import BaseRecord


class Record(BaseRecord):

    @property
    def id(self):
        return self._record.get('eventID')

    @property
    def name(self):
        return self._record.get('eventName')

    @property
    def source(self):
        return self._record.get('eventSource')

    @property
    def source_arn(self):
        return self._record.get('eventSourceARN')

    @property
    def region(self):
        return self._record.get('awsRegion')

    @property
    def version(self):
        return self._record.get('eventVersion')

    @property
    def invoke_identity_arn(self):
        return self._record.get('invokeIdentityArn')

    @property
    def schema_version(self):
        return self._record.get('kinesis', {}).get('kinesisSchemaVersion')

    @property
    def partition_key(self):
        return self._record.get('kinesis', {}).get('partitionKey')

    @property
    def time_stamp(self):
        return self._record.get('kinesis', {}).get('approximateArrivalTimestamp')

    @property
    def sequence_number(self):
        return self._record.get('kinesis', {}).get('sequenceNumber')

    @property
    def data(self):
        b64_decoded = base64.b64decode(self._record.get('kinesis', {}).get('data')).decode('utf-8')
        return JsonHelper.decode(b64_decoded)

    @property
    def body(self):
        return self.data

    @property
    def operation(self):
        return self.UNKNOWN

    def __str__(self):
        return str({
            'id': self.id,
            'name': self.name,
            'source': self.source,
            'source_arn': self.source_arn,
            'region': self.region,
            'version': self.version,
            'invoke_identity_arn': self.invoke_identity_arn,
            'schema_version': self.schema_version,
            'partition_key': self.partition_key,
            'time_stamp': self.time_stamp,
            'sequence_number': self.sequence_number,
            'data': self.data,
            'body': self.body,
            'operation': self.operation
        })
