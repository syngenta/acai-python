from acai.apigateway.requirements import requirements

@requirements(required_route='/user/{user_id}/item')
def get(request, response):
    response.body = {'pattern_mvvm_user_id_item': request.path_params}
    return response
