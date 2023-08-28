import unittest

from acai_aws.common.records.exception import RecordException

from tests.mocks.mq import mock_event
from tests.mocks.mq.mock_functions import mock_mq_full, before_call, after_call, call_list


class MQRequirementsTest(unittest.TestCase):
    basic_event = mock_event.get_basic()

    def test_mq_decorator_with_basic_requirements(self):
        expected = {'mq_full': [True]}
        result = mock_mq_full(self.basic_event, None)
        self.assertDictEqual(result, expected)

    def test_mq_decorator_with_full_requirements(self):
        expected = {'mq_full': [True]}
        result = mock_mq_full(self.basic_event, None)
        self.assertDictEqual(result, expected)
        self.assertTrue(before_call.has_been_called)
        self.assertTrue(after_call.has_been_called)
        self.assertEqual('before', call_list[0])
        self.assertEqual('after', call_list[1])
