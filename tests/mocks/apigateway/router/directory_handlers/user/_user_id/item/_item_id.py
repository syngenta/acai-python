from acai_aws.apigateway.requirements import requirements

@requirements(required_route='/user/{user_id}/item/{item_id}')
def get(request, response):
    response.body = {'directory_user_id_item_id': request.path_params}
    return response
