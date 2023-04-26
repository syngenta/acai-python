import abc

from acai.common.record_exception import RecordException
from acai.common.validator import Validator


class BaseRecordsEvent(abc.ABC):

    def __init__(self, event, context=None, **kwargs):
        self._event = event
        self._context = context
        self._kwargs = kwargs
        self._records = []
        self.data_class = None
        self._validator = Validator(**kwargs)

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
            elif self._kwargs.get('raise_operation_error'):
                raise RecordException(record=record, message=f'record did not meet operation requirement; required: {operations}, received: {record.operation}')
        self._reset_records(validated)

    def _validate_record_body(self):
        validated = []
        for record in self._records:
            errors = self._validator.validate_record_body(record.body, self._kwargs.get('required_body'))
            if len(errors) != 0 and self._kwargs.get('raise_body_error'):
                raise RecordException(record=record, message=f'record did not meet body requirement; errors: {errors}')
            if len(errors) == 0:
                validated.append(record)
        self._reset_records(validated)

    def _reset_records(self, validated):
        self._records.clear()
        self._records = validated

    def __str__(self):
        return str([str(record) for record in self.records])
