from acai_aws.apigateway.requirements import requirements

@requirements(required_route='/bad/dynamic/{id}')
def post(_, response):
    response.body = {'pattern_dynamic_bad': True}
    return response

@requirements(required_route='/bad_dynamic/{id')
def get(_, response):
    response.body = {'pattern_dynamic_bad': True}
    return response
