from acai_aws.apigateway.requirements import requirements

@requirements()
def get(_, response):
    response.body = {'router_pattern_optional': True}
    return response
