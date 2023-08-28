import base64

from acai_aws.common.json_helper import JsonHelper
from acai_aws.base.record import BaseRecord


class Record(BaseRecord):

    @property
    def message_id(self):
        return self._record.get('messageID')

    @property
    def message_type(self):
        return self._record.get('messageType')

    @property
    def data(self):
        b64_decoded = base64.b64decode(self._record.get('data')).decode('utf-8')
        return JsonHelper.decode(b64_decoded)

    @property
    def delivery_mode(self):
        return self._record.get('deliveryMode')

    @property
    def reply_to(self):
        return self._record.get('replyTo')

    @property
    def record_type(self):
        return self._record.get('type')

    @property
    def expiration(self):
        return self._record.get('expiration')

    @property
    def priority(self):
        return self._record.get('priority')

    @property
    def correlation_id(self):
        return self._record.get('correlationId')

    @property
    def redelivered(self):
        return self._record.get('redelivered')

    @property
    def destination(self):
        return self._record.get('destination')

    @property
    def properties(self):
        return self._record.get('properties')

    @property
    def time_stamp(self):
        return self._record.get('timestamp')

    @property
    def in_time(self):
        return self._record.get('brokerInTime')

    @property
    def out_time(self):
        return self._record.get('brokerOutTime')

    @property
    def operation(self):
        return self.UNKNOWN

    @property
    def body(self):
        return self.data

    def __str__(self):
        return str({
            'message_id': self.message_id,
            'message_type': self.message_type,
            'delivery_mode': self.delivery_mode,
            'reply_to': self.reply_to,
            'record_type': self.record_type,
            'expiration': self.expiration,
            'priority': self.priority,
            'correlation_id': self.correlation_id,
            'redelivered': self.redelivered,
            'destination': self.destination,
            'properties': self.properties,
            'time_stamp': self.time_stamp,
            'in_time': self.in_time,
            'out_time': self.out_time,
            'data': self.data,
            'body': self.body,
            'operation': self.operation
        })
