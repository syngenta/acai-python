from acai_aws.common.json_helper import JsonHelper
from acai_aws.base.record import BaseRecord


class Record(BaseRecord):

    @property
    def message_id(self):
        return self._record.get('messageId')

    @property
    def receipt_handle(self):
        return self._record.get('receiptHandle')

    @property
    def body(self):
        return JsonHelper.decode(self._record.get('body'))

    @property
    def operation(self):
        return self.UNKNOWN

    @property
    def message_attributes(self):
        return self._record.get('messageAttributes')

    @property
    def attributes(self):
        self._attributes = self._record.get('attributes', {}).copy()
        for key in self.message_attributes:
            value = None
            if self.message_attributes[key].get('StringValue'):
                value = self.message_attributes[key]['StringValue']
            if self.message_attributes[key].get('BinaryValue'):
                value = self.message_attributes[key]['BinaryValue']
            self._attributes[key] = value
        return self._attributes

    @property
    def region(self):
        return self._record.get('awsRegion')

    @property
    def source_arn(self):
        return self._record.get('eventSourceARN')

    @property
    def source(self):
        return self._record.get('eventSource')

    @property
    def md5_of_body(self):
        return self._record.get('md5OfBody')

    def __str__(self):
        return str({
            'message_id': self.message_id,
            'receipt_handle': self.receipt_handle,
            'body': self.body,
            'operation': self.operation,
            'message_attributes': self.message_attributes,
            'attributes': self.attributes,
            'region': self.region,
            'source_arn': self.source_arn,
            'source': self.source,
            'md5_of_body': self.md5_of_body
        })
