from acai.apigateway.requirements import requirements

@requirements(
    auth_required=True
)
def post(request, response):
    response.body = {'router_directory_basic': request.body}
    return response
