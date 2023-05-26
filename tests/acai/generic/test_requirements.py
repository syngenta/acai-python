import unittest

from tests.mocks.generic import mock_event
from tests.mocks.generic.mock_functions import mock_generic_full, before_call, after_call, call_list


class GenericRequirementsTest(unittest.TestCase):
    basic_event = mock_event.get_basic()
    expected = {'generic_full': {'key': 'value'}}

    def test_generic_decorator_with_basic_requirements(self):
        result = mock_generic_full(self.basic_event, None)
        self.assertDictEqual(result, self.expected)

    def test_generic_decorator_with_full_requirements(self):
        result = mock_generic_full(self.basic_event, None)
        self.assertDictEqual(result, self.expected)
        self.assertTrue(before_call.has_been_called)
        self.assertTrue(after_call.has_been_called)
        self.assertEqual('before', call_list[0])
        self.assertEqual('after', call_list[1])
