from acai.apigateway.requirements import requirements

@requirements(required_route='/dynamic/bad/{id}')
def post(request, response):
    response.body = {'directory_dynamic_bad': True}
    return response
