from acai_aws.common import json_helper


class RecordClient:
    def __init__(self, record):
        self._record = record

    @property
    def message_id(self):
        return self._record.get('messageId')

    @property
    def receipt_handle(self):
        return self._record.get('receiptHandle')

    @property
    def body(self):
        return json_helper.try_decode_json(self._record.get('body'))

    @property
    def raw_body(self):
        return self._record.get('body')

    @property
    def attributes(self):
        return self._record.get('attributes')

    @property
    def approximate_receive_count(self):
        return self.attributes['ApproximateReceiveCount']

    @property
    def sent_timestamp(self):
        return self.attributes['SentTimestamp']

    @property
    def sender_id(self):
        return self.attributes['SenderId']

    @property
    def approximate_first_receive_timestamp(self):
        return self.attributes['ApproximateFirstReceiveTimestamp']

    @property
    def raw_message_attributes(self):
        return self._record.get('messageAttributes')

    @property
    def message_attributes(self):
        attributes = {}
        for key in self.raw_message_attributes:
            attributes[key] = self.raw_message_attributes[key].get('stringValue', '')
        return attributes

    @property
    def md5_of_body(self):
        return self._record.get('md5OfBody')

    @property
    def event_source_arn(self):
        return self._record.get('eventSourceARN')

    @property
    def region(self):
        return self._record.get('awsRegion')

    def __str__(self):
        return str({
            'message_id': self.message_id,
            'receipt_handle': self.receipt_handle,
            'body': self.body,
            'raw_body': self.raw_body,
            'attributes': self.attributes,
            'approximate_receive_count': self.approximate_receive_count,
            'sent_timestamp': self.sent_timestamp,
            'sender_id': self.sender_id,
            'approximate_first_receive_timestamp': self.approximate_first_receive_timestamp,
            'message_attributes': self.message_attributes,
            'raw_message_attributes': self.raw_message_attributes,
            'md5_of_body': self.md5_of_body,
            'event_source_arn': self.event_source_arn,
            'region': self.region
        })
