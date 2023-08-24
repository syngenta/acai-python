from acai.apigateway.requirements import requirements


@requirements(
    required_body='some-schema'
)
def post(_, response):
    response.body = {'endpoint_directory_basic': 'post'}
    return response


def patch(_, response):
    response.body = {'endpoint_directory_basic': 'patch'}
    return response


@requirements(
    auth_required=True
)
def get(_, response):
    response.body = {'endpoint_directory_basic': 'get'}
    return response


@requirements(
    required_route='/some/route/{id}'
)
def delete(_, response):
    response.body = {'endpoint_directory_basic': 'delete'}
    return response


@requirements(
    custom_list=[1, 2, 3],
    custom_dict={'key': 'value'},
    custom_simple=1
)
def put(_, response):
    response.body = {'endpoint_directory_basic': 'put'}
    return response


@requirements(
    required_response='somme-response-schema'
)
def search(_, response):
    response.body = {'endpoint_directory_basic': 'search'}
    return response
