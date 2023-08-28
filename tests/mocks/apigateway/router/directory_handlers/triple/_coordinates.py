from acai_aws.apigateway.requirements import requirements

@requirements(required_route='/triple/{x}/{y}/{z}')
def post(request, response):
    response.body = {'directory_triple_coordinates': request.path_params}
    return response
