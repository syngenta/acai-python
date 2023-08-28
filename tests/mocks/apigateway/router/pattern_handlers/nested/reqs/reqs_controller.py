from acai_aws.apigateway.requirements import requirements

@requirements(
    required_body='v1-post-request-test'
)
def post(request, response):
    response.body = {'router_nested_directory_basic': request.body}
    return response


@requirements(
    required_query=['auth_id'],
    available_query=['email', 'name']
)
def get(request, response):
    response.body = {'router_nested_directory_basic': request.body}
    return response


@requirements(
    required_headers=['content-type'],
    available_headers=['correlation-id']
)
def delete(request, response):
    response.body = {'router_nested_directory_basic': request.body}
    return response
