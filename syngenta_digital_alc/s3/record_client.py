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
    def event_version(self):
        return self._record.get('eventVersion')

    @property
    def event_time(self):
        return self._record.get('eventTime')

    @property
    def region(self):
        return self._record.get('awsRegion')

    @property
    def request_parameters(self):
        return self._record.get('requestParameters')

    @property
    def response_elements(self):
        return self._record.get('responseElements')

    @property
    def s3_configuration_id(self):
        return self._record['s3'].get('configurationId')

    @property
    def s3_object(self):
        return self._record['s3'].get('object')

    @property
    def s3_bucket(self):
        return self._record['s3'].get('bucket')

    @property
    def s3_schema_version(self):
        return self._record['s3'].get('s3SchemaVersion')

    def __str__(self):
        return str({
            'event_name': self.event_name,
            'event_source': self.event_source,
            'event_version': self.event_version,
            'event_time': self.event_time,
            'region': self.region,
            'request_parameters': self.request_parameters,
            'response_elements': self.response_elements,
            's3_configuration_id': self.s3_configuration_id,
            's3_object': self.s3_object,
            's3_bucket': self.s3_bucket,
            's3_schema_version': self.s3_schema_version
        })
