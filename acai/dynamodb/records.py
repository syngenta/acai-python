from acai.common.records import CommonRecords
from acai.dynamodb.record import Record


class Records(CommonRecords):

    def __init__(self, event, context=None, **kwargs):
        super().__init__(event, context, **kwargs)
        self._record_class = Record
