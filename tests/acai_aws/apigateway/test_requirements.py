import unittest

from acai_aws.apigateway.request import Request
from acai_aws.apigateway.response import Response

from tests.mocks.apigateway import mock_request
from tests.mocks.apigateway.requirements.basic import post, before_call, after_call, call_order


class ApigatewayRequirementsTest(unittest.TestCase):
    basic_request = mock_request.get_basic()
    expected_data_class_result = {
        'hasErrors': False,
        'response': {
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': '*'
            },
            'statusCode': 200,
            'isBase64Encoded': False,
            'body': {
                'requirements_basic': True
            }
        }
    }

    def test_requirements_decorator_has_attribute(self):
        self.assertTrue(hasattr(post, 'requirements'))

    def test_requirements_runs_before(self):
        request = Request(self.basic_request)
        response = Response()
        post(request, response)
        self.assertTrue(before_call.has_been_called)

    def test_requirements_runs_after(self):
        request = Request(self.basic_request)
        response = Response()
        post(request, response)
        self.assertTrue(after_call.has_been_called)

    def test_requirements_runs_in_correct_order(self):
        request = Request(self.basic_request)
        response = Response()
        post(request, response)
        self.assertEqual('before', call_order[0])
        self.assertEqual('after', call_order[1])

    def test_requirements_passes_after_data_class(self):
        request = Request(self.basic_request)
        response = Response()
        result = post(request, response)
        self.assertEqual(str(self.expected_data_class_result), str(result))
