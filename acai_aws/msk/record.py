import base64

from acai_aws.common.json_helper import JsonHelper
from acai_aws.base.record import BaseRecord


class Record(BaseRecord):

    @property
    def topic(self):
        return self._record.get('topic')

    @property
    def partition(self):
        return self._record.get('partition')

    @property
    def offset(self):
        return self._record.get('offset')

    @property
    def time_stamp(self):
        return self._record.get('timestamp')

    @property
    def time_stamp_type(self):
        return self._record.get('timestampType')

    @property
    def key(self):
        return base64.b64decode(self._record.get('key')).decode('utf-8')

    @property
    def value(self):
        b64_decoded = base64.b64decode(self._record.get('value')).decode('utf-8')
        return JsonHelper.decode(b64_decoded)

    @property
    def headers(self):
        return self._record.get('headers')

    @property
    def operation(self):
        return self.UNKNOWN

    @property
    def body(self):
        return self.value

    def __str__(self):
        return str({
            'topic': self.topic,
            'partition': self.partition,
            'offset': self.offset,
            'time_stamp': self.time_stamp,
            'time_stamp_type': self.time_stamp_type,
            'key': self.key,
            'value': self.value,
            'headers': self.headers,
            'operation': self.operation,
            'body': self.body
        })
