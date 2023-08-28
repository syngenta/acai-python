from acai_aws.apigateway.requirements import requirements

@requirements(
    auth_required=True
)
def post(request, response):
    response.body = {'router_mapping_basic': request.body}
    return response
