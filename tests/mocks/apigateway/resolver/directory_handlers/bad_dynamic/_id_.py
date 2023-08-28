from acai_aws.apigateway.requirements import requirements

@requirements(required_route='/bad/dynamic/{id}')
def post(request, response):
    response.body = {'directory_dynamic_bad': True}
    return response

@requirements(required_route='/bad_dynamic/{id')
def get(request, response):
    response.body = {'directory_dynamic_bad': True}
    return response
