from acai.apigateway.requirements import requirements


@requirements(
    required_body='some-schema'
)
def post(request, response):
    response.body = {'endpoint_directory_basic': 'post'}
    return response


def patch(request, response):
    response.body = {'endpoint_directory_basic': 'patch'}
    return response


@requirements(
    auth_required=True
)
def get(request, response):
    response.body = {'endpoint_directory_basic': 'get'}
    return response


@requirements(
    required_route='/some/route/{id}'
)
def delete(request, response):
    response.body = {'endpoint_directory_basic': 'delete'}
    return response


@requirements(
    custom_list=[1, 2, 3],
    custom_dict={'key': 'value'},
    custom_simple=1
)
def put(request, response):
    response.body = {'endpoint_directory_basic': 'put'}
    return response


@requirements(
    required_response='somme-response-schema'
)
def search(request, response):
    response.body = {'endpoint_directory_basic': 'search'}
    return response
