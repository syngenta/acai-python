from acai.apigateway.requirements import requirements

@requirements(
    auth_required=True
)
def post(request, response):
    response.body = {'router_pattern_basic': request.body}
    return response
