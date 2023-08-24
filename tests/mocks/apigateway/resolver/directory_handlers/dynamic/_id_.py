from acai.apigateway.requirements import requirements

@requirements(required_route='/dynamic/{id}')
def post(request, response):
    response.body = {'directory_dynamic': True}
    return response
