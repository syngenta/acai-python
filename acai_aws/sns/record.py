from acai_aws.common.json_helper import JsonHelper
from acai_aws.base.record import BaseRecord


class Record(BaseRecord):

    @property
    def version(self):
        return self._record.get('EventVersion')

    @property
    def subscription_arn(self):
        return self._record.get('EventSubscriptionArn')

    @property
    def source(self):
        return self._record.get('EventSource')

    @property
    def signature_version(self):
        return self._record.get('Sns', {}).get('SignatureVersion')

    @property
    def timestamp(self):
        return self._record.get('Sns', {}).get('Timestamp')

    @property
    def signature(self):
        return self._record.get('Sns', {}).get('Signature')

    @property
    def signing_cert_url(self):
        return self._record.get('Sns', {}).get('SigningCertUrl')

    @property
    def message_id(self):
        return self._record.get('Sns', {}).get('MessageId')

    @property
    def message(self):
        return self._record.get('Sns', {}).get('Message')

    @property
    def message_attributes(self):
        return self._record.get('Sns', {}).get('MessageAttributes')

    @property
    def attributes(self):
        if not self._attributes:
            for key in self.message_attributes:
                self._attributes[key] = self.message_attributes[key].get('Value')
        return self._attributes

    @property
    def sns_type(self):
        return self._record.get('Sns', {}).get('Type')

    @property
    def unsubscribe_url(self):
        return self._record.get('Sns', {}).get('UnsubscribeUrl')

    @property
    def topic_arn(self):
        return self._record.get('Sns', {}).get('TopicArn')

    @property
    def subject(self):
        return self._record.get('Sns', {}).get('Subject')

    @property
    def body(self):
        return JsonHelper.decode(self.message)

    @property
    def operation(self):
        return self.UNKNOWN

    def __str__(self):
        return str({
            'version': self.version,
            'subscription_arn': self.subscription_arn,
            'source': self.source,
            'timestamp': self.timestamp,
            'signature': self.signature,
            'signing_cert_url': self.signing_cert_url,
            'message_id': self.message_id,
            'message_attributes': self.message_attributes,
            'message': self.message,
            'attributes': self.attributes,
            'sns_type': self.sns_type,
            'unsubscribe_url': self.unsubscribe_url,
            'topic_arn': self.topic_arn,
            'body': self.body,
            'operation': self.operation
        })
