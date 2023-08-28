from acai_aws.base.record import BaseRecord


class Record(BaseRecord):

    @property
    def name(self):
        return self._record.get('eventName')

    @property
    def source(self):
        return self._record.get('eventSource')

    @property
    def version(self):
        return self._record.get('eventVersion')

    @property
    def time(self):
        return self._record.get('eventTime')

    @property
    def region(self):
        return self._record.get('awsRegion')

    @property
    def request(self):
        return self._record.get('requestParameters')

    @property
    def response(self):
        return self._record.get('responseElements')

    @property
    def configuration_id(self):
        return self._record['s3'].get('configurationId')

    @property
    def object(self):
        return self._record['s3'].get('object')

    @property
    def bucket(self):
        return self._record['s3'].get('bucket', {}).get('name')

    @property
    def bucket_arn(self):
        return self._record['s3'].get('bucket', {}).get('arn')

    @property
    def bucket_owner(self):
        return self._record['s3'].get('bucket', {}).get('ownerIdentity', {}).get('principalId')

    @property
    def key(self):
        return self._record['s3'].get('object', {}).get('key')

    @property
    def schema_version(self):
        return self._record['s3'].get('s3SchemaVersion')

    @property
    def user_identity(self):
        return self._record['userIdentity'].get('principalId')

    @property
    def operation(self):
        if 'ObjectCreated' in self.name:
            return self.CREATED
        if 'ObjectRemoved' in self.name:
            return self.DELETED
        return self.UNKNOWN

    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, body):
        self._body = body

    def __str__(self):
        return str({
            'name': self.name,
            'source': self.source,
            'version': self.version,
            'time': self.time,
            'region': self.region,
            'request': self.request,
            'response': self.response,
            'configuration_id': self.configuration_id,
            'object': self.object,
            'bucket': self.bucket,
            'schema_version': self.schema_version
        })
