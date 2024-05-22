from acai_aws.apigateway.requirements import requirements


@requirements(
    required_route='/nested_1/nested_2/{id}',
    required_body={
        'type': 'object',
        'required': [],
        'additionalProperties': False,
        'properties': {
            'grower_id': {'type': 'string'},
            'body': {'type': 'object'},
            'dict': {'type': 'boolean'}
        },
    }
)
def patch(_, response):
    response.body = {'nested-2-id': True}
    return response


@requirements(
    required_route='/nested_1/nested_2/{id}',
)
def delete(_, response):
    response.body = {'nested-2-id': False}
    return response
