from acai_aws.apigateway.custom_exceptions import BeforeAllException
from acai_aws.apigateway.handler_requirements import handler_requirements


@handler_requirements()
def run_pass(request, response):  # pylint: disable=unused-argument
    pass


@handler_requirements()
def run_fail(request, response):  # pylint: disable=unused-argument
    raise BeforeAllException(code=401, key_path='headers:x-api-key', message='you need an api key')
