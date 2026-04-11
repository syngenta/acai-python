from acai_aws.common import logger
from acai_aws.common.records.exception import RecordException
from acai_aws.base.no_data import NoDataClass
from acai_aws.base.placeholder import PlaceHolderRecord
from acai_aws.common.validator import Validator


class FailureMode:
    SILENT_IGNORE = 'silent_ignore'
    LOG_WARN = 'log_warn'
    RAISE_ERROR = 'raise_error'
    RETURN_FAILURE = 'return_failure'


_VALID_FAILURE_MODES = {
    FailureMode.SILENT_IGNORE,
    FailureMode.LOG_WARN,
    FailureMode.RAISE_ERROR,
    FailureMode.RETURN_FAILURE,
}


class BaseRecordsEvent:

    def __init__(self, event, context=None, **kwargs):
        self._event = event
        self._context = context
        self._kwargs = kwargs
        self._records = []
        self._invalid_records = []
        self._record_class = PlaceHolderRecord
        self.__data_class = NoDataClass
        self.__validator = Validator(**kwargs)
        self.__validated = False

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
        if not self.__validated:
            self.validate()
        return self.data_classes if self.data_class is not None else self._records

    @property
    def invalid_records(self):
        return self._invalid_records

    @property
    def batch_failure_response_key(self):
        return 'batchItemFailures'

    def batch_item_failures(self):
        return [
            record.batch_item_identifier
            for record, _errors in self._invalid_records
            if getattr(record, 'batch_item_identifier', None) is not None
        ]

    def build_short_circuit_response(self):
        return None

    def validate(self):
        if self.__validated:
            return
        self.__validated = True
        self._build_records()
        failures = []
        failures.extend(self._run_operation_check())
        self._post_operation_hook()
        failures.extend(self._run_body_check())
        self._dispatch_failures(failures)

    def _build_records(self):
        self._records = [self._record_class(record) for record in self.raw_records]

    def _post_operation_hook(self):
        return

    def _run_operation_check(self):
        if not self._kwargs.get('operations'):
            return []
        failures = []
        surviving = []
        for record in self._records:
            if record.operation in self._kwargs['operations']:
                surviving.append(record)
            else:
                failures.append((record, [{
                    'key_path': 'operation',
                    'message': f'record operation "{record.operation}" not in allowed {self._kwargs["operations"]}',
                }]))
        self._records = surviving
        return failures

    def _run_body_check(self):
        if not self._kwargs.get('required_body'):
            return []
        failures = []
        surviving = []
        for record in self._records:
            errors = self.__validator.validate_record_body(record.body, self._kwargs['required_body'])
            if errors:
                failures.append((record, errors))
            else:
                surviving.append(record)
        self._records = surviving
        return failures

    def _dispatch_failures(self, failures):
        if not failures:
            return
        mode = self.resolve_failure_mode()
        if mode == FailureMode.RAISE_ERROR:
            record, errors = failures[0]
            raise RecordException(
                record=record,
                message=f'record failed validation; errors: {errors}',
            )
        if mode == FailureMode.LOG_WARN:
            for record, errors in failures:
                logger.log(level='WARN', log={
                    'message': 'acai_aws: record filtered by validation',
                    'record_id': getattr(record, 'batch_item_identifier', None),
                    'errors': errors,
                })
            return
        if mode == FailureMode.RETURN_FAILURE:
            self._invalid_records = failures
            return
        # FailureMode.SILENT_IGNORE — nothing to do

    def resolve_failure_mode(self):
        mode = self._kwargs.get('failure_mode')
        if mode and mode not in _VALID_FAILURE_MODES:
            raise ValueError(
                f'acai_aws: unknown failure_mode "{mode}"; '
                f'expected one of {sorted(_VALID_FAILURE_MODES)}'
            )
        if mode:
            return mode
        if self._kwargs.get('raise_body_error') or self._kwargs.get('raise_operation_error'):
            if not getattr(BaseRecordsEvent, '_deprecation_logged', False):
                logger.log(level='WARN', log={
                    'message': (
                        'acai_aws: raise_body_error/raise_operation_error are deprecated; '
                        'use failure_mode="raise_error" instead'
                    ),
                })
                BaseRecordsEvent._deprecation_logged = True
            return FailureMode.RAISE_ERROR
        return FailureMode.SILENT_IGNORE

    def __str__(self):
        return str([str(record) for record in self.records])
