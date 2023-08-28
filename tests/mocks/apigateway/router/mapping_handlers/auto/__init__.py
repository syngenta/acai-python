from acai_aws.apigateway.requirements import requirements

@requirements()
def post(request, response):
    response.body = {'router_mapping_auto': request.body}
    return response

@requirements()
def get(request, response):
    response.body = {'page_number': 1, 'data': {'id': '2'}}
    return response

@requirements(
    required_response='v1-required-response'
)
def patch(request, response):
    response.body = {'page_number': 1, 'data': {'id': '2'}}
    return response

@requirements()
def put(request, response):
    response.body = {'page_number': 1, 'bad-put': {'id': 2}}
    return response

@requirements(
     required_response='v1-required-response'
)
def delete(request, response):
    response.body = {'page_number': 1, 'bad-delete': {'id': 2}}
    return response
