from acai.apigateway.exception import ApiException
from acai.apigateway.requirements import requirements


@requirements()
def post(request, response):
    response.body = {'router_pattern_basic': request.body}
    raise ApiException(code=418, key_path='crazy_error', message='I am a teapot')
    return response
