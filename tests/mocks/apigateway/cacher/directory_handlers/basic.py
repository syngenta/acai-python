from acai_aws.apigateway.requirements import requirements


@requirements()
def post(_, response):
    response.body = {'cacher_directory': 'request'}
    return response

@requirements()
def get(_, response):
    response.body = {'page_number': 1, 'data': {'id': '2'}}
    return response

@requirements(
    required_response='v1-required-response'
)
def patch(_, response):
    response.body = {'page_number': 1, 'data': {'id': '2'}}
    return response

@requirements()
def put(_, response):
    response.body = {'page_number': 1, 'bad-put': {'id': 2}}
    return response

@requirements(
     required_response='v1-required-response'
)
def delete(_, response):
    response.body = {'page_number': 1, 'bad-delete': {'id': 2}}
    return response
