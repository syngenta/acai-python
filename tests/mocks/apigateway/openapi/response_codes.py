from acai_aws.apigateway.requirements import requirements


@requirements(
    required_query=['email'],
    response_codes={
        200: 'User exists',
        204: 'User does not exist'
    }
)
def get(_, response):
    response.body = {'exists': True}
    return response


@requirements(
    required_response={
        'type': 'object',
        'required': ['id'],
        'properties': {
            'id': {'type': 'string'}
        }
    },
    response_codes={
        200: 'Resource found',
        204: 'Resource not found'
    }
)
def post(_, response):
    response.body = {'id': '123'}
    return response
