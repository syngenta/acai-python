from acai.common.records.base import BaseRecords
from acai.dynamodb.record import Record


class Records(BaseRecords):

    def __init__(self, event, context=None, **kwargs):
        super().__init__(event, context, **kwargs)
        self._record_class = Record
