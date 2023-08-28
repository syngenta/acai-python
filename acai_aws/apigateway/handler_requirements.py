from acai_aws.apigateway.request_client import RequestClient
from acai_aws.apigateway.response_client import ResponseClient
from acai_aws.apigateway.request_validator import RequestValidator

def handler_requirements(**kwargs):
    def decorator_func(func):
        def wrapper(event, context, schema_path = ''):
            request = RequestClient(event, context)
            response = ResponseClient()
            validator = RequestValidator(request, response, schema_path)
            validator.validate_request(**kwargs)
            if not response.has_errors:
                func(request, response)
            return response.response
        return wrapper
    return decorator_func
