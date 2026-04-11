import json

from acai_aws.base.event import BaseRecordsEvent
from acai_aws.alb.record import Record


class Event(BaseRecordsEvent):

    def __init__(self, event, context=None, **kwargs):
        super().__init__(event, context, **kwargs)
        self._record_class = Record
        self.__validation_errors = []

    @property
    def raw_records(self):
        return [self._event]

    @property
    def validation_errors(self):
        return self.__validation_errors

    def _dispatch_failures(self, failures):
        flattened = []
        for _record, errors in failures:
            flattened.extend(errors)
        self.__validation_errors = flattened

    def build_short_circuit_response(self):
        if not self.__validation_errors:
            return None
        return {
            'statusCode': 400,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'errors': self.__validation_errors}),
            'isBase64Encoded': False,
        }
