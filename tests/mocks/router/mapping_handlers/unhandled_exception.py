from acai.apigateway.requirements import requirements


@requirements()
def post(request, response):
    response.body = {'router_mapping_basic': request.body}
    raise UnknownException(code=418, key_path='crazy_error', message='I am a teapot')
    return response
