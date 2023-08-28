from acai_aws.base.event import BaseRecordsEvent
from acai_aws.sqs.record import Record


class Event(BaseRecordsEvent):

    def __init__(self, event, context=None, **kwargs):
        super().__init__(event, context, **kwargs)
        self._record_class = Record
