from acai_aws.apigateway.requirements import requirements

from tests.mocks.common.mock_pydantic_class import UserRequest


@requirements(
    auth_required=True,
    required_body=UserRequest
)
def post(_, response):
    response.body = {'dynamic': True}
    return response


@requirements(
    auth_required=True,
    required_headers=['x-dynamic-key'],
    required_response={
        'type': 'object',
        'required': ['dynamic_id', 'dynamic_bool', 'dynamic_message'],
        'additionalProperties': False,
        'properties': {
            'dynamic_id': {'type': 'int'},
            'dynamic_bool': {'type': 'boolean'},
            'dynamic_message': {'type': 'string'}
        },
    }
)
def get(_, response):
    response.body = {'dynamic': True}
    return response
