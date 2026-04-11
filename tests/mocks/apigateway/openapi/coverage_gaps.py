from pydantic import BaseModel

from acai_aws.apigateway.requirements import requirements


class Address(BaseModel):
    street: str
    city: str


class UserWithNestedDefs(BaseModel):
    id: int
    name: str
    address: Address


class SimpleResponse(BaseModel):
    ok: bool


@requirements(
    auth_required=True,
    required_body=UserWithNestedDefs,
    required_response=SimpleResponse,
)
def post(_, response):
    response.body = {'ok': True}
    return response


class NotAPydanticModel:
    pass


@requirements(required_body=NotAPydanticModel)
def put(_, response):
    response.body = {}
    return response
