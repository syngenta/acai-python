import copy
import json
import logging
import unittest
from unittest.mock import patch

from pydantic import BaseModel, PositiveInt

from acai_aws.base.event import BaseRecordsEvent, FailureMode
from acai_aws.common.records.exception import RecordException
from acai_aws.common.records.requirements import requirements, _merge_batch_item_failures
from acai_aws.common.validator import Validator
from acai_aws.sqs.event import Event as SQSEvent

from tests.mocks.sqs import mock_event as sqs_mock_event
from tests.mocks.alb import mock_event as alb_mock_event


class NotificationPreferences(BaseModel):
    lang: str
    sms: bool
    email: bool
    push: bool


class StrictUser(BaseModel):
    id: PositiveInt
    email: str


def _sqs_event_with_bad_and_good_records():
    event = copy.deepcopy(sqs_mock_event.get_basic())
    good = event['Records'][0]
    bad = copy.deepcopy(good)
    bad['messageId'] = 'bad-message-id'
    bad['body'] = '{"lang": "en-us", "sms": "not-a-bool", "email": true, "push": true}'
    event['Records'].append(bad)
    return event


class ValidatorPydanticSupportTest(unittest.TestCase):

    def test_validate_record_body_pydantic_pass(self):
        validator = Validator()
        errors = validator.validate_record_body(
            {'lang': 'en-us', 'sms': True, 'email': True, 'push': True},
            NotificationPreferences,
        )
        self.assertEqual(errors, [])

    def test_validate_record_body_pydantic_fail_returns_key_path_and_message(self):
        validator = Validator()
        errors = validator.validate_record_body(
            {'lang': 'en-us', 'sms': 'nope', 'email': True, 'push': True},
            NotificationPreferences,
        )
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0]['key_path'], 'sms')
        self.assertIn('message', errors[0])

    def test_validate_record_body_dict_schema_uses_key_path_field(self):
        validator = Validator()
        schema = {
            'type': 'object',
            'properties': {'amount': {'type': 'integer'}},
            'required': ['amount'],
        }
        errors = validator.validate_record_body({}, schema)
        self.assertEqual(len(errors), 1)
        self.assertIn('key_path', errors[0])
        self.assertIn('message', errors[0])


class FailureModeDispatchTest(unittest.TestCase):

    def setUp(self):
        self.event = _sqs_event_with_bad_and_good_records()

    def test_silent_ignore_is_default(self):
        sqs_event = SQSEvent(self.event, required_body=NotificationPreferences)
        self.assertEqual(sqs_event.resolve_failure_mode(), FailureMode.SILENT_IGNORE)
        self.assertEqual(len(sqs_event.records), 1)
        self.assertEqual(sqs_event.invalid_records, [])

    def test_raise_error_mode_raises_eagerly(self):
        sqs_event = SQSEvent(
            self.event,
            required_body=NotificationPreferences,
            failure_mode=FailureMode.RAISE_ERROR,
        )
        with self.assertRaises(RecordException):
            sqs_event.validate()

    def test_return_failure_mode_collects_invalid_records(self):
        sqs_event = SQSEvent(
            self.event,
            required_body=NotificationPreferences,
            failure_mode=FailureMode.RETURN_FAILURE,
        )
        sqs_event.validate()
        self.assertEqual(len(sqs_event.records), 1)
        self.assertEqual(len(sqs_event.invalid_records), 1)
        failures = sqs_event.batch_item_failures()
        self.assertEqual(failures, [{'itemIdentifier': 'bad-message-id'}])

    def test_log_warn_mode_logs_and_filters(self):
        sqs_event = SQSEvent(
            self.event,
            required_body=NotificationPreferences,
            failure_mode=FailureMode.LOG_WARN,
        )
        with patch('acai_aws.base.event.logger.log') as mock_log:
            sqs_event.validate()
        self.assertEqual(len(sqs_event.records), 1)
        self.assertEqual(sqs_event.invalid_records, [])
        mock_log.assert_called()
        call_kwargs = mock_log.call_args.kwargs
        self.assertEqual(call_kwargs['level'], 'WARN')
        self.assertIn('errors', call_kwargs['log'])

    def test_unknown_failure_mode_raises_value_error(self):
        sqs_event = SQSEvent(
            self.event,
            required_body=NotificationPreferences,
            failure_mode='bogus',
        )
        with self.assertRaises(ValueError):
            sqs_event.validate()

    def test_deprecated_raise_body_error_still_raises(self):
        BaseRecordsEvent._deprecation_logged = False
        sqs_event = SQSEvent(
            self.event,
            required_body=NotificationPreferences,
            raise_body_error=True,
        )
        with self.assertRaises(RecordException):
            sqs_event.validate()

    def test_operation_check_uses_failure_mode(self):
        event = _sqs_event_with_bad_and_good_records()
        sqs_event = SQSEvent(
            event,
            operations=['created'],
            failure_mode=FailureMode.RETURN_FAILURE,
        )
        sqs_event.validate()
        self.assertEqual(len(sqs_event.records), 0)
        self.assertEqual(len(sqs_event.invalid_records), 2)


class BatchItemIdentifierTest(unittest.TestCase):

    def test_sqs_identifier_uses_message_id(self):
        event = _sqs_event_with_bad_and_good_records()
        sqs_event = SQSEvent(
            event,
            required_body=NotificationPreferences,
            failure_mode=FailureMode.RETURN_FAILURE,
        )
        sqs_event.validate()
        self.assertEqual(
            sqs_event.batch_item_failures(),
            [{'itemIdentifier': 'bad-message-id'}],
        )


class MergeBatchItemFailuresTest(unittest.TestCase):

    def _event_with_one_bad_record(self):
        event = _sqs_event_with_bad_and_good_records()
        sqs_event = SQSEvent(
            event,
            required_body=NotificationPreferences,
            failure_mode=FailureMode.RETURN_FAILURE,
        )
        sqs_event.validate()
        return sqs_event

    def test_merge_wraps_none_handler_return(self):
        sqs_event = self._event_with_one_bad_record()
        result = _merge_batch_item_failures(None, sqs_event)
        self.assertEqual(
            result,
            {'batchItemFailures': [{'itemIdentifier': 'bad-message-id'}]},
        )

    def test_merge_appends_to_existing_list(self):
        sqs_event = self._event_with_one_bad_record()
        handler_result = {'batchItemFailures': [{'itemIdentifier': 'A'}]}
        merged = _merge_batch_item_failures(handler_result, sqs_event)
        self.assertEqual(
            merged['batchItemFailures'],
            [{'itemIdentifier': 'A'}, {'itemIdentifier': 'bad-message-id'}],
        )

    def test_merge_dedupes_identical_identifiers(self):
        sqs_event = self._event_with_one_bad_record()
        handler_result = {'batchItemFailures': [{'itemIdentifier': 'bad-message-id'}]}
        merged = _merge_batch_item_failures(handler_result, sqs_event)
        self.assertEqual(
            merged['batchItemFailures'],
            [{'itemIdentifier': 'bad-message-id'}],
        )

    def test_merge_preserves_other_dict_keys(self):
        sqs_event = self._event_with_one_bad_record()
        handler_result = {'ok': True, 'batchItemFailures': []}
        merged = _merge_batch_item_failures(handler_result, sqs_event)
        self.assertTrue(merged['ok'])
        self.assertEqual(merged['batchItemFailures'], [{'itemIdentifier': 'bad-message-id'}])

    def test_merge_noop_when_no_framework_failures(self):
        event = sqs_mock_event.get_basic()
        sqs_event = SQSEvent(
            event,
            required_body=NotificationPreferences,
            failure_mode=FailureMode.RETURN_FAILURE,
        )
        sqs_event.validate()
        handler_result = {'ok': True}
        merged = _merge_batch_item_failures(handler_result, sqs_event)
        self.assertEqual(merged, {'ok': True})


class DecoratorIntegrationTest(unittest.TestCase):

    def test_decorator_merges_framework_failures_into_return(self):
        captured = {}

        @requirements(
            required_body=NotificationPreferences,
            failure_mode=FailureMode.RETURN_FAILURE,
        )
        def handler(event):
            captured['record_count'] = len(event.records)
            return {'batchItemFailures': [{'itemIdentifier': 'handler-detected'}]}

        event = _sqs_event_with_bad_and_good_records()
        result = handler(event, context=None)

        self.assertEqual(captured['record_count'], 1)
        identifiers = {item['itemIdentifier'] for item in result['batchItemFailures']}
        self.assertEqual(identifiers, {'handler-detected', 'bad-message-id'})

    def test_decorator_eager_validation_raises_before_handler(self):
        called = {'handler': False}

        @requirements(
            required_body=NotificationPreferences,
            failure_mode=FailureMode.RAISE_ERROR,
        )
        def handler(event):
            called['handler'] = True
            return {}

        event = _sqs_event_with_bad_and_good_records()
        with self.assertRaises(RecordException):
            handler(event, context=None)
        self.assertFalse(called['handler'])

    def test_decorator_silent_ignore_leaves_return_untouched(self):
        @requirements(required_body=NotificationPreferences)
        def handler(event):
            return {'processed': len(event.records)}

        event = _sqs_event_with_bad_and_good_records()
        result = handler(event, context=None)
        self.assertEqual(result, {'processed': 1})


class ALBDecoratorTest(unittest.TestCase):

    def test_alb_invalid_body_returns_http_400_short_circuit(self):
        handler_was_called = {'yes': False}

        @requirements(required_body=StrictUser)
        def handler(event):
            handler_was_called['yes'] = True
            return {'statusCode': 200, 'body': '{}'}

        event = alb_mock_event.get_basic()
        result = handler(event, context=None)

        self.assertFalse(handler_was_called['yes'])
        self.assertEqual(result['statusCode'], 400)
        self.assertEqual(result['headers']['Content-Type'], 'application/json')
        body = json.loads(result['body'])
        self.assertIn('errors', body)
        self.assertTrue(len(body['errors']) > 0)
        for error in body['errors']:
            self.assertIn('key_path', error)
            self.assertIn('message', error)

    def test_alb_valid_body_runs_handler(self):
        schema = {
            'type': 'object',
            'properties': {
                'business_id': {'type': 'string'},
                'decision': {'type': 'string'},
                'completed': {'type': 'string'},
            },
        }

        @requirements(required_body=schema)
        def handler(event):
            return {'statusCode': 200, 'body': 'ok'}

        event = alb_mock_event.get_basic()
        result = handler(event, context=None)
        self.assertEqual(result['statusCode'], 200)

    def test_alb_no_required_body_runs_handler(self):
        @requirements()
        def handler(event):
            return {'statusCode': 200, 'body': 'pass-through'}

        event = alb_mock_event.get_basic()
        result = handler(event, context=None)
        self.assertEqual(result['statusCode'], 200)


if __name__ == '__main__':
    unittest.main()
