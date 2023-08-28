from dynamodb_json import json_util as ddb_json

from acai_aws.base.record import BaseRecord


class Record(BaseRecord):

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
    def version(self):
        return self._record.get('eventVersion')

    @property
    def id(self):
        return self._record.get('eventID')

    @property
    def region(self):
        return self._record.get('awsRegion')

    @property
    def stream_view_type(self):
        return self._record['dynamodb'].get('StreamViewType')

    @property
    def sequence_number(self):
        return self._record['dynamodb'].get('SequenceNumber')

    @property
    def size_bytes(self):
        return self._record['dynamodb'].get('SizeBytes')

    @property
    def keys(self):
        return ddb_json.loads(self._record['dynamodb'].get('Keys', {}))

    @property
    def old_image(self):
        return ddb_json.loads(self._record['dynamodb'].get('OldImage', {}))

    @property
    def new_image(self):
        return ddb_json.loads(self._record['dynamodb'].get('NewImage', {}))

    @property
    def approximate_creation_time(self):
        return self._record['dynamodb'].get('ApproximateCreationDateTime')

    @property
    def body(self):
        return self.new_image

    @property
    def operation(self):
        if self.new_image and not self.old_image:
            return self.CREATED
        if self.new_image and self.old_image:
            return self.UPDATED
        if not self.new_image and self.old_image:
            return self.DELETED
        return self.UNKNOWN

    def __str__(self):
        return str({
            'id': self.id,
            'name': self.name,
            'version': self.version,
            'region': self.region,
            'source_arn': self.source_arn,
            'source': self.source,
            'dynamodb_keys': self.keys,
            'dynamodb_stream_view_type': self.stream_view_type,
            'dynamodb_sequence_number': self.sequence_number,
            'dynamodb_size_bytes': self.size_bytes,
            'dynamodb_old_image': self.old_image,
            'dynamodb_new_image': self.new_image,
            'approximate_creation_time': self.approximate_creation_time
        })
