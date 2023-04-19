from acai.apigateway.requirements import requirements

@requirements(required_route='/bad/dynamic/{id}')
def post(_, response):
    response.body = {'pattern_mvvm_dynamic_bad': True}
    return response

@requirements(required_route='/bad_dynamic/{id')
def get(_, response):
    response.body = {'pattern_mvvm_dynamic_bad': True}
    return response
