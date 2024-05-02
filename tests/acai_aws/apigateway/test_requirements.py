import unittest

from acai_aws.apigateway.exception import ApiTimeOutException
from acai_aws.apigateway.request import Request
from acai_aws.apigateway.response import Response

from tests.mocks.apigateway import mock_request
from tests.mocks.apigateway.requirements import basic


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
        self.assertTrue(hasattr(basic.post, 'requirements'))

    def test_requirements_runs_before(self):
        request = Request(self.basic_request)
        response = Response()
        basic.post(request, response)
        self.assertTrue(basic.before_call.has_been_called)

    def test_requirements_runs_after(self):
        request = Request(self.basic_request)
        response = Response()
        basic.post(request, response)
        self.assertTrue(basic.after_call.has_been_called)

    def test_requirements_runs_in_correct_order(self):
        request = Request(self.basic_request)
        response = Response()
        basic.post(request, response)
        self.assertEqual('before', basic.call_order[0])
        self.assertEqual('after', basic.call_order[1])

    def test_requirements_passes_after_data_class(self):
        request = Request(self.basic_request)
        response = Response()
        result = basic.post(request, response)
        self.assertEqual(str(self.expected_data_class_result), str(result))
    
    def test_requirements_global_timeout_raises_exception(self):
        request = Request(self.basic_request, None, 1)
        response = Response()
        try:
            basic.get(request, response)
            self.assertTrue(False)
        except ApiTimeOutException as error:
            self.assertTrue(isinstance(error, ApiTimeOutException))
        
    def test_requirements_local_timeout_raises_exception(self):
        event = mock_request.get_dynamic_event(method='patch')
        request = Request(event)
        response = Response()
        try:
            basic.patch(request, response)
            self.assertTrue(False)
        except ApiTimeOutException as error:
            self.assertTrue(isinstance(error, ApiTimeOutException))
        
    def test_requirements_local_overwrites_global_timeout_setting(self):
        event = mock_request.get_dynamic_event(method='patch')
        request = Request(event, None, 10)
        response = Response()
        try:
            basic.patch(request, response)
            self.assertTrue(False)
        except ApiTimeOutException as error:
            self.assertTrue(isinstance(error, ApiTimeOutException))    
