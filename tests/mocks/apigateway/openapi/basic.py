from acai_aws.apigateway.requirements import requirements

from tests.mocks.common.mock_pydantic_class import UserRequest
# required_route='/user/{user_id}/item'
#


@requirements(
    available_query=['first', 'last'],
    required_query=['basic_id']
)
def get(_, response):
    response.body = {'basic-openapigenerator': True}
    return response


@requirements(
    required_body=UserRequest
)
def post(_, response):
    response.body = {'basic-openapigenerator': True}
    return response
