import unittest

from acai_aws.common.records.exception import RecordException

from tests.mocks.dynamodb import mock_event
from tests.mocks.dynamodb.mock_functions import mock_ddb_full, mock_ddb_basic, mock_ddb_operation_ignore, mock_ddb_operation_raise, before_call, after_call, \
    call_list


class DynamoDBRequirementsTest(unittest.TestCase):
    created_record = mock_event.get_created_event()

    def test_ddb_decorator_with_basic_requirements(self):
        expected = {'ddb_basic': ['INSERT']}
        result = mock_ddb_basic(self.created_record, None)
        self.assertDictEqual(result, expected)

    def test_ddb_decorator_with_full_requirements(self):
        expected = {'ddb_full': [True]}
        result = mock_ddb_full(self.created_record, None)
        self.assertDictEqual(result, expected)
        self.assertTrue(before_call.has_been_called)
        self.assertTrue(after_call.has_been_called)
        self.assertEqual('before', call_list[0])
        self.assertEqual('after', call_list[1])

    def test_ddb_decorator_ignore_non_matching_operation(self):
        expected = {'ddb_operation_ignore': []}
        result = mock_ddb_operation_ignore(self.created_record, None)
        self.assertDictEqual(result, expected)

    def test_ddb_decorator_ignore_non_matching_operation_error(self):
        try:
            mock_ddb_operation_raise(self.created_record, None)
            self.assertTrue(False)
        except RecordException as record_error:
            self.assertTrue(isinstance(record_error, RecordException))
