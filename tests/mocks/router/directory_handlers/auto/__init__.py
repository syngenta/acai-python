from acai.apigateway.requirements import requirements

@requirements()
def post(request, response):
    response.body = {'router_directory_auto': request.body}
    return response
