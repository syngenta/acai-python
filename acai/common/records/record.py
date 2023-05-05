from acai.common.json_helper import JsonHelper
from acai.base.record import BaseRecord


class CommonRecord(BaseRecord):

    @property
    def body(self):
        return JsonHelper.decode(self._record)

    @property
    def operation(self):
        return self.UNKNOWN
