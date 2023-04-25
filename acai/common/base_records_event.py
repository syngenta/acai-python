import abc

from acai.common.record_exception import RecordException


class BaseRecordsEvent(abc.ABC):

    def __init__(self, event, context=None, **kwargs):
        self._event = event
        self._context = context
        self._kwargs = kwargs
        self._records = []
        self.data_class = None

    @property
    def event(self):
        return self._event

    @property
    def context(self):
        return self._context

    @property
    def raw_records(self):
        return self._event.get('Records', [])

    @property
    @abc.abstractmethod
    def records(self):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def data_classes(self):
        raise NotImplementedError

    def _validate_operations(self, operations):
        validated = []
        for record in self._records:
            if record.operation in operations:
                validated.append(record)
            elif self._kwargs.get('operation_error'):
                raise RecordException(record=record, message=f'record did not meet operation requirement; required: {operations}, received: {record.operation}')
        self._records.clear()
        self._records = validated

    def __str__(self):
        return str([str(record) for record in self.records])
