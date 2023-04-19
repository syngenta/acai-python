from acai.apigateway.requirements import requirements

@requirements(required_route='/dynamic/{id}')
def post(_, response):
    response.body = {'pattern_mvc_dynamic': True}
    return response
