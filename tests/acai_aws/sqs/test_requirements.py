import unittest

from acai_aws.common.records.exception import RecordException

from tests.mocks.sqs import mock_event
from tests.mocks.sqs.mock_functions import mock_sqs_full, before_call, after_call, call_list


class SQSRequirementsTest(unittest.TestCase):
    basic_event = mock_event.get_basic()

    def test_sqs_decorator_with_basic_requirements(self):
        expected = {'sqs_full': [True]}
        result = mock_sqs_full(self.basic_event, None)
        self.assertDictEqual(result, expected)

    def test_sqs_decorator_with_full_requirements(self):
        expected = {'sqs_full': [True]}
        result = mock_sqs_full(self.basic_event, None)
        self.assertDictEqual(result, expected)
        self.assertTrue(before_call.has_been_called)
        self.assertTrue(after_call.has_been_called)
        self.assertEqual('before', call_list[0])
        self.assertEqual('after', call_list[1])
