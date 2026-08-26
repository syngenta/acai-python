from acai_aws.apigateway.requirements import requirements


@requirements()
def post(request, response):
    # request.json is the strict parser; malformed input is a client contract
    # error and must surface as a 400, not an unhandled 500.
    response.body = {'router_mapping_strict_json': request.json}
    return response
