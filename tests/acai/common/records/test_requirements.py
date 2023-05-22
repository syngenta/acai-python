import unittest

from acai.common.records.exception import RecordException

from tests.mocks.common.mock_functions import mock_func, mock_func_verbose


class CommonRequirementsTest(unittest.TestCase):
    event = {'key': 'value'}
    context = None

    def test_decorator_with_unknown_type_verbose(self):
        expected = {'event': [self.event]}
        result = mock_func_verbose(self.event, self.context)
        self.assertDictEqual(result, expected)
