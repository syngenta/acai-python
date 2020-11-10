from dynamodb_json import json_util as ddb_json

class RecordClient:

    def __init__(self, record):
        self._record = record

    @property
    def event_name(self):
        return self._record.get('eventName')

    @property
    def event_source(self):
        return self._record.get('eventSource')

    @property
    def event_source_arn(self):
        return self._record.get('eventSourceARN')

    @property
    def event_version(self):
        return self._record.get('eventVersion')

    @property
    def event_id(self):
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

    def __str__(self):
        return str({
            'event_id': self.event_id,
            'event_name': self.event_name,
            'event_version': self.event_version,
            'region': self.region,
            'event_source_arn': self.event_source_arn,
            'event_source': self.event_source,
            'dynamodb_keys': self.dynamodb_keys,
            'dynamodb_stream_view_type': self.dynamodb_stream_view_type,
            'dynamodb_sequence_number': self.dynamodb_sequence_number,
            'dynamodb_size_bytes': self.dynamodb_size_bytes,
            'dynamodb_old_image': self.dynamodb_old_image,
            'dynamodb_new_image': self.dynamodb_new_image,
            'approximate_creation_time': self.approximate_creation_time,
        })
