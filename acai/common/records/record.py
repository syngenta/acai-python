from acai.base.record import BaseRecord


class CommonRecord(BaseRecord):

    @property
    def body(self):
        return self._record

    @property
    def operation(self):
        return self.UNKNOWN
