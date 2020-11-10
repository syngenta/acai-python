from syngenta_digital_alc.common import json_helper


class RecordClient:

    def __init__(self, record):
        self._record = record

    @property
    def event_source(self):
        return self._record.get('EventSource')

    @property
    def event_version(self):
        return self._record.get('EventVersion')

    @property
    def event_subscription_arn(self):
        return self._record.get('EventSubscriptionArn')

    @property
    def sns_signature_version(self):
        return self._record['Sns'].get('SignatureVersion')

    @property
    def sns_timestamp(self):
        return self._record['Sns'].get('Timestamp')

    @property
    def sns_signature(self):
        return self._record['Sns'].get('Signature')

    @property
    def sns_signing_cert_url(self):
        return self._record['Sns'].get('SigningCertUrl')

    @property
    def sns_message(self):
        return json_helper.try_decode_json(self._record['Sns'].get('Message'))

    @property
    def sns_message_attributes(self):
        return self._record['Sns'].get('MessageAttributes')

    @property
    def sns_type(self):
        return self._record['Sns'].get('Type')

    @property
    def sns_unsubscribe_url(self):
        return self._record['Sns'].get('UnsubscribeUrl')

    @property
    def sns_topic_arn(self):
        return self._record['Sns'].get('TopicArn')

    @property
    def sns_subject(self):
        return self._record['Sns'].get('Subject')

    def __str__(self):
        return str({
            'event_source': self.event_source,
            'event_version': self.event_version,
            'event_subscription_arn': self.event_subscription_arn,
            'sns_signature_version': self.sns_signature_version,
            'sns_timestamp': self.sns_timestamp,
            'sns_signature': self.sns_signature,
            'sns_signing_cert_url': self.sns_signing_cert_url,
            'sns_message': self.sns_message,
            'sns_type': self.sns_type,
            'sns_subject': self.sns_subject
        })
