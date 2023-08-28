import unittest

from acai_aws.common.records.exception import RecordException

from tests.mocks.s3 import mock_event
from tests.mocks.s3.mock_functions import mock_s3_full, mock_s3_basic, mock_s3_operation_ignore, mock_s3_operation_raise, before_call, after_call, call_list


class S3RequirementsTest(unittest.TestCase):
    basic_event = mock_event.get_basic()

    def test_s3_decorator_with_basic_requirements(self):
        expected = {'s3_basic': ['ObjectCreated: Put']}
        result = mock_s3_basic(self.basic_event, None)
        self.assertDictEqual(result, expected)

    def test_s3_decorator_with_full_requirements(self):
        expected = {'s3_full': [True]}
        result = mock_s3_full(self.basic_event, None)
        self.assertDictEqual(result, expected)
        self.assertTrue(before_call.has_been_called)
        self.assertTrue(after_call.has_been_called)
        self.assertEqual('before', call_list[0])
        self.assertEqual('after', call_list[1])

    def test_s3_decorator_ignore_non_matching_operation(self):
        expected = {'s3_operation_ignore': []}
        result = mock_s3_operation_ignore(self.basic_event, None)
        self.assertDictEqual(result, expected)

    def test_s3_decorator_ignore_non_matching_operation_error(self):
        try:
            mock_s3_operation_raise(self.basic_event, None)
            self.assertTrue(False)
        except RecordException as record_error:
            self.assertTrue(isinstance(record_error, RecordException))
