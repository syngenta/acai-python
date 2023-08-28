from acai_aws.common.records.exception import RecordException
from acai_aws.base.no_data import NoDataClass
from acai_aws.base.placeholder import PlaceHolderRecord
from acai_aws.common.validator import Validator


class BaseRecordsEvent:

    def __init__(self, event, context=None, **kwargs):
        self._event = event
        self._context = context
        self._kwargs = kwargs
        self._records = []
        self._record_class = PlaceHolderRecord
        self.__data_class = NoDataClass
        self.__validator = Validator(**kwargs)

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
    def data_class(self):
        if issubclass(self.__data_class, NoDataClass):
            return None
        return self.__data_class

    @data_class.setter
    def data_class(self, data_class):
        self.__data_class = data_class

    @property
    def data_classes(self):
        return [self.data_class(record=record) for record in self._records]

    @property
    def records(self):
        self._records = [self._record_class(record) for record in self.raw_records]
        self._validate_operations()
        self._validate_record_body()
        return self.data_classes if self.data_class is not None else self._records

    def _validate_operations(self):
        if not self._kwargs.get('operations'):
            return
        validated = []
        for record in self._records:
            if record.operation in self._kwargs['operations']:
                validated.append(record)
            elif self._kwargs.get('raise_operation_error'):
                raise RecordException(record=record, message=f'record did not meet operation requirement; required: {self._kwargs["operations"]}, received: {record.operation}')
        self._reset_records(validated)

    def _validate_record_body(self):
        if not self._kwargs.get('required_body'):
            return
        validated = []
        for record in self._records:
            errors = self.__validator.validate_record_body(record.body, self._kwargs.get('required_body'))
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
